class CircuitCanvasView(QGraphicsView):
    # Signals to be observed by ModelView
    gatePlaced = Signal(str, QPointF, str)               # gate_type, scene_pos, gate_id
    gateSelected = Signal(str)                           # gate_id
    connectionStarted = Signal(str)                      # source_pin_id
    connectionPreview = Signal(QPointF)                  # current mouse scene pos while dragging
    connectionCompleted = Signal(str, str)               # source_pin_id, target_pin_id
    itemMoved = Signal(str, QPointF)                     # gate_id, new_scene_pos

    def __init__(self, parent=None):
        super().__init__(parent)
        self._canvas_settings = CanvasSettings()

        self._scene = QGraphicsScene(self)
        # attach self reference to scene to allow GateItem -> scene -> canvas callbacks
        self._scene._canvas_view = self
        self.setScene(self._scene)

        # render hints
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        # interaction state
        self._panning = False
        self._last_pan_pos = None
        self._current_scale = 1.0

        # connection interaction
        self._rubber_band: Optional[ConnectionItem] = None
        self._connection_source_pin_id: Optional[str] = None

        # index of items by id
        self._items_by_id: Dict[str, QGraphicsItem] = {}

        # view setup
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        # appearance
        self.setBackgroundBrush(QBrush(self._canvas_settings.BACKGROUND_COLOR))

    def drawBackground(self, painter: QPainter, rect):
        super().drawBackground(painter, rect)
        left = int(rect.left()) - (int(rect.left()) % self._canvas_settings.GRID_SIZE)
        top = int(rect.top()) - (int(rect.top()) % self._canvas_settings.GRID_SIZE)

        painter.setPen(QPen(self._canvas_settings.GRID_COLOR, 0))
        x = left
        while x < rect.right():
            painter.drawLine(x, rect.top(), x, rect.bottom())
            x += self._canvas_settings.GRID_SIZE

        y = top
        while y < rect.bottom():
            painter.drawLine(rect.left(), y, rect.right(), y)
            y += self._canvas_settings.GRID_SIZE

        # draw thicker major lines
        major = self._canvas_settings.GRID_SIZE * self._canvas_settings.GRID_MAJOR_FACTOR
        painter.setPen(QPen(self._canvas_settings.GRID_DARK_COLOR, 0))
        x = int(rect.left()) - (int(rect.left()) % major)
        while x < rect.right():
            painter.drawLine(x, rect.top(), x, rect.bottom())
            x += major
        y = int(rect.top()) - (int(rect.top()) % major)
        while y < rect.bottom():
            painter.drawLine(rect.left(), y, rect.right(), y)
            y += major

    def wheelEvent(self, event):
        # Zoom centered at mouse pointer. Scrolling changes scale according to settings.
        delta = event.angleDelta().y()
        if delta == 0:
            return
        factor = self._canvas_settings.ZOOM_STEP if delta > 0 else 1 / self._canvas_settings.ZOOM_STEP
        new_scale = self._current_scale * factor
        if new_scale < self._canvas_settings.ZOOM_MIN or new_scale > self._canvas_settings.ZOOM_MAX:
            return
        self.scale(factor, factor)
        self._current_scale = new_scale
        event.accept()

    def reset_zoom(self):
        self.resetTransform()
        self._current_scale = 1.0

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            # start panning
            self._panning = True
            self._last_pan_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._panning and self._last_pan_pos is not None:
            delta = event.pos() - self._last_pan_pos
            self._last_pan_pos = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            event.accept()
            return

        # if a connection drag is active, update rubberband
        if self._rubber_band is not None:
            scene_pos = self.mapToScene(event.pos())
            self._update_rubberband_preview(scene_pos)
            self.connectionPreview.emit(scene_pos)

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton and self._panning:
            self._panning = False
            self._last_pan_pos = None
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            return
        super().mouseReleaseEvent(event)

    # ---------------------- Drag & Drop (placing gates) ---------------------- #
    def dragEnterEvent(self, event):
        mime = event.mimeData()
        if mime.hasFormat("application/x-gate-type") or mime.hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        # Expecting mime text containing the gate type (eg. "AND", "OR", "NOT", "SWITCH")
        mime = event.mimeData()
        if mime.hasFormat("application/x-gate-type"):
            gate_type = str(mime.data("application/x-gate-type"), encoding="utf-8")
        else:
            gate_type = mime.text()

        scene_pos = self.mapToScene(event.position().toPoint() if hasattr(event, 'position') else event.pos())
        # create visual GateItem and emit gatePlaced for ModelView to create model
        gate_item = GateItem(gate_type)
        if self._canvas_settings.SNAP_TO_GRID:
            scene_pos = self._snap_to_grid(scene_pos)
        gate_item.setPos(scene_pos)
        self._scene.addItem(gate_item)
        self._items_by_id[gate_item.gate_id] = gate_item

        # connect some signals so Canvas can re-emit to ModelView
        gate_item.selectedChanged.connect(lambda gid, sel: self.gateSelected.emit(gid))
        gate_item.positionChanged.connect(lambda gid, pos: self.itemMoved.emit(gid, pos))

        self.gatePlaced.emit(gate_type, scene_pos, gate_item.gate_id)
        event.acceptProposedAction()

    # ---------------------- Connection handling ---------------------- #
    def _start_connection(self, source_pin_id: str):
        # initialize rubberband
        self._connection_source_pin_id = source_pin_id
        self._rubber_band = ConnectionItem(QPointF(0, 0), QPointF(0, 0))
        self._scene.addItem(self._rubber_band)
        self.connectionStarted.emit(source_pin_id)

    def _update_rubberband_preview(self, scene_pos: QPointF):
        if self._rubber_band is None or self._connection_source_pin_id is None:
            return
        # compute source pin scene position if available
        source_pin_item = self._find_pin_item(self._connection_source_pin_id)
        if source_pin_item is None:
            return
        src_pos = source_pin_item.mapToScene(source_pin_item.boundingRect().center())
        self._rubber_band.update_path(src_pos, scene_pos)

    def _finish_connection(self, pin_id: str, release_scene_pos: QPointF):
        # if pin_id is the same as source, cancel
        if self._connection_source_pin_id is None:
            # nothing to finish
            return
        # find pin under release position
        target_pin_item = self._find_pin_item_at(release_scene_pos)
        if target_pin_item and target_pin_item.pin_id != self._connection_source_pin_id:
            # finalize permanent connection item
            src_item = self._find_pin_item(self._connection_source_pin_id)
            if src_item is None:
                self._cancel_rubberband()
                return
            src_pos = src_item.mapToScene(src_item.boundingRect().center())
            tgt_pos = target_pin_item.mapToScene(target_pin_item.boundingRect().center())
            conn = ConnectionItem(src_pos, tgt_pos)
            self._scene.addItem(conn)
            # re-emit for ModelView to actually connect model pins
            self.connectionCompleted.emit(self._connection_source_pin_id, target_pin_item.pin_id)
        # cleanup rubberband
        self._cancel_rubberband()

    def _cancel_rubberband(self):
        if self._rubber_band is not None:
            self._scene.removeItem(self._rubber_band)
            self._rubber_band = None
        self._connection_source_pin_id = None

    # ---------------------- Lookup helpers ---------------------- #
    def _find_pin_item(self, pin_id: str) -> Optional[PinItem]:
        # naive linear search - optimize later if necessary
        for item in self._scene.items():
            if isinstance(item, PinItem) and item.pin_id == pin_id:
                return item
        return None

    def _find_pin_item_at(self, scene_pos: QPointF) -> Optional[PinItem]:
        # check items at the scene position (small tolerance)
        items = self._scene.items(scene_pos)
        for it in items:
            if isinstance(it, PinItem):
                return it
        return None

    # ---------------------- Grid snapping ---------------------- #
    def _snap_to_grid(self, scene_pos: QPointF) -> QPointF:
        gs = self._canvas_settings.GRID_SIZE
        x = round(scene_pos.x() / gs) * gs
        y = round(scene_pos.y() / gs) * gs
        return QPointF(x, y)

    # ---------------------- Public API for view manipulation ---------------------- #
    def add_gate_visual(self, gate_type: str, scene_pos: QPointF) -> str:
        """Create a visual gate from code (not only via drag and drop).
        Returns gate_id so callers can reference the visual later.
        """
        gate_item = GateItem(gate_type)
        if self._canvas_settings.SNAP_TO_GRID:
            scene_pos = self._snap_to_grid(scene_pos)
        gate_item.setPos(scene_pos)
        self._scene.addItem(gate_item)
        self._items_by_id[gate_item.gate_id] = gate_item
        gate_item.selectedChanged.connect(lambda gid, sel: self.gateSelected.emit(gid))
        gate_item.positionChanged.connect(lambda gid, pos: self.itemMoved.emit(gid, pos))
        return gate_item.gate_id

    def remove_visual(self, item_id: str):
        item = self._items_by_id.get(item_id)
        if item:
            self._scene.removeItem(item)
            del self._items_by_id[item_id]

    def clear_canvas(self):
        self._scene.clear()
        self._items_by_id.clear()