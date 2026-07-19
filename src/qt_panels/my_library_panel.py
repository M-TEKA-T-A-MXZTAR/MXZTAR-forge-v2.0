#!/usr/bin/env python3
"""Visible source-art library for MXZTAR Forge v2.0.

My Library presents every discovered source as a selectable card, uses bounded
rebuildable thumbnails, and hands the exact original SourceArtItem to Agent
Workflows without modifying the source.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from PySide6.QtCore import QSize, Qt, QThread, Signal
from PySide6.QtGui import QIcon, QImage, QImageIOHandler, QImageReader, QPixmap
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QProgressBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.source_preview_cache import (
    obsolete_source_preview_paths,
    prune_source_preview_cache,
    source_preview_cache_path,
)
from core.project_session import ProjectSession
from core.project_source_intake import import_source_copy, scan_project_source_art
from core.source_library import (
    SourceArtItem,
    format_size,
    known_source_dirs,
    scan_source_art,
)


PREVIEW_MAX_WIDTH = 1600
PREVIEW_MAX_HEIGHT = 1200
CARD_ICON_SIZE = QSize(180, 120)
CARD_GRID_SIZE = QSize(210, 165)


class ThumbnailLoader(QThread):
    """Decode library previews sequentially without blocking the Qt event loop."""

    preview_ready = Signal(int, object, object, str)

    def __init__(self, sources, preview_loader, parent=None):
        super().__init__(parent)
        self._sources = tuple(sources)
        self._preview_loader = preview_loader

    def run(self):
        for index, source in enumerate(self._sources):
            if self.isInterruptionRequested():
                break
            image, error = self._preview_loader(source)
            if self.isInterruptionRequested():
                break
            self.preview_ready.emit(index, source, image, error)


class LibraryDiscoveryThread(QThread):
    """Discover sources outside the Qt main thread."""

    discovered = Signal(object, str)

    def __init__(self, source_provider, parent=None):
        super().__init__(parent)
        self._source_provider = source_provider

    def run(self):
        try:
            sources = self._source_provider()
        except Exception as exc:
            self.discovered.emit([], str(exc))
            return
        if not self.isInterruptionRequested():
            self.discovered.emit(sources, "")


class SourceIntakeThread(QThread):
    """Run one transactional project source intake off the Qt main thread."""

    completed = Signal(object, str)

    def __init__(self, project_session, source_path, parent=None):
        super().__init__(parent)
        self._project_session = project_session
        self._source_path = Path(source_path)

    def run(self):
        try:
            result = import_source_copy(self._project_session, self._source_path)
        except Exception as exc:
            self.completed.emit(None, str(exc))
        else:
            self.completed.emit(result, "")


class MyLibraryPanel(QWidget):
    status_changed = Signal(str)
    source_selected = Signal(object)
    background_idle = Signal()
    intake_active_changed = Signal(bool)

    def __init__(self, project_session: ProjectSession | None = None):
        super().__init__()
        self.project_session = project_session or ProjectSession()
        self.source_items = []
        self._preview_image = QImage()
        self._preview_source_path = None
        self._thumbnail_loader = None
        self._discovery_thread = None
        self._intake_thread = None
        self._pending_intake_message = None
        self._refresh_pending = False

        title = QLabel("My Library")
        title.setStyleSheet("font-size: 24px; font-weight: 700;")

        intro = QLabel(
            "Every known source appears below. Select a card to inspect it, then send the "
            "unchanged original to Agent Workflows."
        )
        intro.setWordWrap(True)
        intro.setStyleSheet("color: #cfcfcf;")

        boundary = QLabel(
            "Current stage: Source Art. Input files remain authoritative; thumbnails are "
            "rebuildable UI cache."
        )
        boundary.setWordWrap(True)
        boundary.setStyleSheet("color: #d6c27a;")

        refresh_button = QPushButton("Refresh Library")
        refresh_button.setToolTip("Rescan known source folders without changing their contents.")
        refresh_button.clicked.connect(self.refresh_library)

        self.open_folder_button = QPushButton("Open Containing Folder")
        self.open_folder_button.clicked.connect(self.open_containing_folder)

        self.use_button = QPushButton("Use in Agent Workflows")
        self.use_button.setToolTip(
            "Select this exact original source in Agent Workflows without copying or moving it."
        )
        self.use_button.clicked.connect(self.use_in_agent_workflows)

        self.import_button = QPushButton("Import into Active Project")
        self.import_button.setToolTip(
            "Copy a supported image into the active writable project. The external file remains unchanged."
        )
        self.import_button.clicked.connect(self.choose_project_source)

        action_row = QHBoxLayout()
        action_row.addWidget(self.use_button)
        action_row.addWidget(self.import_button)
        action_row.addWidget(self.open_folder_button)
        action_row.addWidget(refresh_button)
        action_row.addStretch(1)

        self.source_grid = QListWidget()
        self.source_grid.setViewMode(QListWidget.ViewMode.IconMode)
        self.source_grid.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.source_grid.setMovement(QListWidget.Movement.Static)
        self.source_grid.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.source_grid.setIconSize(CARD_ICON_SIZE)
        self.source_grid.setGridSize(CARD_GRID_SIZE)
        self.source_grid.setWordWrap(True)
        self.source_grid.setSpacing(8)
        self.source_grid.setMinimumHeight(250)
        self.source_grid.setStyleSheet(
            "QListWidget { background-color: #181818; border: 1px solid #3a3a3a; }"
            "QListWidget::item { color: #f2f2f2; padding: 6px; }"
            "QListWidget::item:selected { background-color: #5a4d24; border: 1px solid #d6c27a; }"
        )
        self.source_grid.currentItemChanged.connect(self.update_selection)

        self.preview_label = QLabel("Select a source card.")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumSize(240, 160)
        self.preview_label.setMaximumSize(360, 220)
        self.preview_label.setStyleSheet(
            "background-color: #181818; border: 1px solid #3a3a3a; padding: 4px;"
        )

        self.details = QTextEdit()
        self.details.setReadOnly(True)
        self.details.setMinimumHeight(160)
        self.details.setMaximumHeight(220)

        selected_frame = QFrame()
        selected_frame.setFrameShape(QFrame.Shape.StyledPanel)
        selected_layout = QHBoxLayout()
        selected_layout.setContentsMargins(6, 6, 6, 6)
        selected_layout.addWidget(self.preview_label, 0)
        selected_layout.addWidget(self.details, 1)
        selected_frame.setLayout(selected_layout)

        self.status_label = QLabel("Ready.")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("color: #d6c27a;")

        self.intake_progress = QProgressBar()
        self.intake_progress.setRange(0, 0)
        self.intake_progress.setVisible(False)
        self.intake_progress.setToolTip(
            "Indeterminate progress: file size and image decoding time vary by source."
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(8)
        layout.addWidget(title)
        layout.addWidget(intro)
        layout.addWidget(boundary)
        layout.addLayout(action_row)
        layout.addWidget(self.source_grid, 1)
        layout.addWidget(QLabel("Selected source:"))
        layout.addWidget(selected_frame, 0)
        layout.addWidget(self.status_label)
        layout.addWidget(self.intake_progress)
        self.setLayout(layout)

        self.update_project_controls()
        self.refresh_library()

    def selected_source(self) -> SourceArtItem | None:
        current = self.source_grid.currentItem()
        if current is None:
            return None
        item = current.data(Qt.ItemDataRole.UserRole)
        return item if isinstance(item, SourceArtItem) else None

    def refresh_library(self):
        if self.has_active_intake():
            self._refresh_pending = True
            self.set_status("Source intake is active; refresh will run after it finishes.")
            return
        if self._discovery_thread is not None and self._discovery_thread.isRunning():
            self._refresh_pending = True
            self._discovery_thread.requestInterruption()
            self.set_status("Stopping the current source discovery before refreshing…")
            return
        if self._thumbnail_loader is not None and self._thumbnail_loader.isRunning():
            self._refresh_pending = True
            self._thumbnail_loader.requestInterruption()
            self.set_status("Stopping the current thumbnail scan before refreshing…")
            return

        self.set_status("Discovering legacy and active-project sources…")
        self._discovery_thread = LibraryDiscoveryThread(self.discover_sources, self)
        self._discovery_thread.discovered.connect(self._discovery_finished)
        self._discovery_thread.finished.connect(self._discovery_thread_finished)
        self._discovery_thread.start()
        self.update_project_controls()

    def discover_sources(self):
        return list(scan_project_source_art(self.project_session)) + list(scan_source_art())

    def _discovery_finished(self, sources, error):
        if error:
            self.source_items = []
            self.source_grid.clear()
            self.clear_selection()
            self.set_status(f"Could not discover project sources safely: {error}")
            return
        previous = self.selected_source()
        previous_path = previous.path if previous is not None else None
        self.source_grid.blockSignals(True)
        self.source_grid.clear()
        self.source_items = list(sources)

        selected_item = None
        for source in self.source_items:
            card = QListWidgetItem(source.label)
            card.setData(Qt.ItemDataRole.UserRole, source)
            card.setToolTip(f"{source.path}\n{format_size(source.size_bytes)}")
            self.source_grid.addItem(card)
            if selected_item is None or (
                previous_path is not None and source.path == previous_path
            ):
                selected_item = card

        self.source_grid.blockSignals(False)

        if not self.source_items:
            self.clear_selection()
            message = self._pending_intake_message or (
                "No source art found. Paste supported images into the MXZTAR Forge Input folder."
            )
            self._pending_intake_message = None
            self.set_status(message)
            return

        self.source_grid.setCurrentItem(selected_item)
        self.update_selection()
        self.set_status(
            f"Showing all {len(self.source_items)} source-art file(s); loading thumbnails…"
        )
        self._thumbnail_loader = ThumbnailLoader(
            self.source_items, self.preview_image_for, self
        )
        self._thumbnail_loader.preview_ready.connect(self._apply_thumbnail)
        self._thumbnail_loader.finished.connect(self._thumbnail_loading_finished)
        self._thumbnail_loader.start()

    def _discovery_thread_finished(self):
        thread = self._discovery_thread
        self._discovery_thread = None
        if thread is not None:
            thread.deleteLater()
        self.update_project_controls()
        if self._refresh_pending and not self.has_active_thumbnail_loading():
            self._refresh_pending = False
            self.refresh_library()
            return
        if not self.has_active_thumbnail_loading():
            self.background_idle.emit()

    def _apply_thumbnail(self, index, source, image, error):
        if index >= self.source_grid.count():
            return
        card = self.source_grid.item(index)
        if card.data(Qt.ItemDataRole.UserRole) != source:
            return

        if not image.isNull():
            card_image = image.scaled(
                CARD_ICON_SIZE,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            card.setIcon(QIcon(QPixmap.fromImage(card_image)))
            if self.selected_source() == source:
                self._preview_image = image
                self._preview_source_path = source.path
                self.render_selected_preview()
        elif error:
            card.setToolTip(f"{card.toolTip()}\nPreview: {error}")
            if self.selected_source() == source:
                self.show_preview_error(error)

    def _thumbnail_loading_finished(self):
        loader = self._thumbnail_loader
        self._thumbnail_loader = None
        if loader is not None:
            loader.deleteLater()
        self.update_project_controls()
        if self._refresh_pending:
            self._refresh_pending = False
            self.refresh_library()
            return
        message = self._pending_intake_message or (
            f"Showing all {len(self.source_items)} source-art file(s)."
        )
        self._pending_intake_message = None
        self.set_status(message)
        self.background_idle.emit()

    def has_active_thumbnail_loading(self) -> bool:
        loader = self._thumbnail_loader
        discovery = self._discovery_thread
        return (
            (loader is not None and loader.isRunning())
            or (discovery is not None and discovery.isRunning())
        )

    def request_thumbnail_shutdown(self) -> None:
        """Request non-blocking thumbnail shutdown; completion emits background_idle."""
        loader = self._thumbnail_loader
        discovery = self._discovery_thread
        active = False
        self._refresh_pending = False
        if discovery is not None and discovery.isRunning():
            discovery.requestInterruption()
            active = True
        if loader is not None and loader.isRunning():
            loader.requestInterruption()
            active = True
        if not active:
            self.background_idle.emit()

    def set_project_state(self, _state=None):
        self.update_project_controls()
        self.refresh_library()

    def update_project_controls(self):
        self.import_button.setEnabled(
            self.project_session.is_writable
            and not self.has_active_intake()
            and not self.has_active_thumbnail_loading()
        )

    def choose_project_source(self):
        if not self.project_session.is_writable:
            self.set_status("Open or create a writable project before importing source art.")
            return
        path, _filter = QFileDialog.getOpenFileName(
            self,
            "Import Source into Active Project",
            str(Path.home()),
            "Supported images (*.png *.jpg *.jpeg *.webp *.tif *.tiff)",
        )
        if path:
            self.start_project_intake(Path(path))

    def start_project_intake(self, source_path: Path) -> bool:
        if self.has_active_intake():
            self.set_status("A project source intake is already active.")
            return False
        if not self.project_session.is_writable:
            self.set_status("A writable project session is required for source intake.")
            return False
        if self.has_active_thumbnail_loading():
            self.set_status("Wait for source discovery and thumbnail loading to finish first.")
            return False
        self._intake_thread = SourceIntakeThread(
            self.project_session, source_path, self
        )
        self._intake_thread.completed.connect(self._intake_completed)
        self._intake_thread.finished.connect(self._intake_thread_finished)
        self.intake_progress.setVisible(True)
        self.intake_active_changed.emit(True)
        self.update_project_controls()
        self.set_status(
            f"Importing {source_path.name}: copying, hashing, validating, and creating a bounded preview…"
        )
        self._intake_thread.start()
        return True

    def _intake_completed(self, result, error):
        if error:
            self._pending_intake_message = (
                f"Source intake failed; no success is claimed: {error}"
            )
            self.set_status(self._pending_intake_message)
            return
        action = "Already present" if result.duplicate else "Imported"
        self._pending_intake_message = (
            f"{action} project source {result.record['original_filename']} "
            f"as {result.record['asset_id']}."
        )
        self.set_status(self._pending_intake_message)

    def _intake_thread_finished(self):
        thread = self._intake_thread
        self._intake_thread = None
        if thread is not None:
            thread.deleteLater()
        self.intake_progress.setVisible(False)
        self.intake_active_changed.emit(False)
        self.update_project_controls()
        self._refresh_pending = False
        self.refresh_library()

    def has_active_intake(self) -> bool:
        thread = self._intake_thread
        return thread is not None and thread.isRunning()

    def update_selection(self, *_):
        item = self.selected_source()

        if item is None:
            self.clear_selection()
            return

        self.use_button.setEnabled(True)
        self.open_folder_button.setEnabled(True)
        self.details.setPlainText(
            f"Name: {item.path.name}\n"
            f"Path: {item.path}\n"
            f"Library section: {item.folder_name}\n"
            f"Authority: {item.authority}\n"
            f"Type: {item.suffix}\n"
            f"Size: {format_size(item.size_bytes)}\n\n"
            "Original remains unchanged. Selection does not imply ownership, licence "
            "validation, or approval. Agent output is stored separately."
        )

        try:
            cached = QImage(str(source_preview_cache_path(item.path)))
        except OSError:
            cached = QImage()
        if not cached.isNull():
            self._preview_image = cached
            self._preview_source_path = item.path
            self.render_selected_preview()
        else:
            self._preview_image = QImage()
            self._preview_source_path = None
            self.preview_label.setPixmap(QPixmap())
            self.preview_label.setText("Thumbnail loading…\nOriginal remains selectable.")

    def preview_image_for(self, item: SourceArtItem) -> tuple[QImage, str]:
        if item.preview_path is not None:
            image = QImage(str(item.preview_path))
            if image.isNull():
                return QImage(), "The declared project preview could not be decoded."
            return image, ""
        try:
            cache_path = source_preview_cache_path(item.path)
        except OSError as exc:
            return QImage(), f"Could not inspect source metadata: {exc}"

        cached = QImage(str(cache_path))
        if not cached.isNull():
            return cached, ""

        reader = QImageReader(str(item.path))
        reader.setAutoTransform(True)
        source_size = reader.size()

        if not source_size.isValid():
            return QImage(), "Image dimensions are unavailable; safe decode cannot be confirmed."

        requires_downscale = (
            source_size.width() > PREVIEW_MAX_WIDTH
            or source_size.height() > PREVIEW_MAX_HEIGHT
        )

        if requires_downscale:
            if not reader.supportsOption(QImageIOHandler.ImageOption.ScaledSize):
                return (
                    QImage(),
                    f"{source_size.width()}×{source_size.height()} source cannot prove "
                    "a memory-bounded Qt preview decode.",
                )

            reader.setScaledSize(
                source_size.scaled(
                    QSize(PREVIEW_MAX_WIDTH, PREVIEW_MAX_HEIGHT),
                    Qt.AspectRatioMode.KeepAspectRatio,
                )
            )

        image = reader.read()
        if image.isNull():
            return QImage(), reader.errorString() or "Qt could not decode this format."

        self.save_preview_cache(image, cache_path, item.path)
        return image, ""

    def save_preview_cache(self, image: QImage, cache_path: Path, source_path: Path):
        temporary_path = cache_path.with_name(f"{cache_path.name}.tmp")

        try:
            if not image.save(str(temporary_path), "PNG"):
                return

            temporary_path.replace(cache_path)

            for obsolete_path in obsolete_source_preview_paths(source_path, cache_path):
                try:
                    obsolete_path.unlink()
                except OSError:
                    # Obsolete cache cleanup is best-effort and must not block preview use.
                    pass

            prune_source_preview_cache(keep_paths=(cache_path,))
        except OSError:
            # Cache failure must not block source selection or workflow handoff.
            pass

    def show_preview_error(self, detail: str):
        self._preview_image = QImage()
        self._preview_source_path = None
        self.preview_label.setPixmap(QPixmap())
        self.preview_label.setText(
            f"Preview unavailable.\n{detail}\nOriginal remains selectable."
        )

    def render_selected_preview(self):
        if self._preview_image.isNull():
            return

        pixmap = QPixmap.fromImage(self._preview_image)
        target = self.preview_label.size()
        scaled = pixmap.scaled(
            max(1, target.width() - 8),
            max(1, target.height() - 8),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.preview_label.setText("")
        self.preview_label.setPixmap(scaled)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.render_selected_preview()

    def clear_selection(self):
        self.use_button.setEnabled(False)
        self.open_folder_button.setEnabled(False)
        self._preview_image = QImage()
        self._preview_source_path = None
        self.preview_label.setPixmap(QPixmap())
        self.preview_label.setText("No source selected.")
        folders = "\n".join(f"- {path}" for path in known_source_dirs())
        self.details.setPlainText(
            "Supported: PNG, JPG, JPEG, WEBP, BMP, TIF, TIFF\n\n"
            f"Known source folders:\n{folders}"
        )

    def use_in_agent_workflows(self):
        item = self.selected_source()

        if item is None:
            self.set_status("Select a source card before opening Agent Workflows.")
            return

        if not item.path.exists():
            self.set_status(f"Selected source no longer exists: {item.path}")
            return

        self.source_selected.emit(item)
        self.set_status(f"Sent original source to Agent Workflows: {item.path.name}")

    def open_containing_folder(self):
        item = self.selected_source()

        if item is None:
            self.set_status("Select a source card before opening its folder.")
            return

        try:
            subprocess.Popen(["xdg-open", str(item.path.parent)])
            self.set_status(f"Opened source folder: {item.path.parent}")
        except Exception as exc:
            self.set_status(f"Could not open source folder: {exc}")

    def set_status(self, message: str):
        self.status_label.setText(message)
        self.status_changed.emit(message)
