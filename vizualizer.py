"""
Heavy Metals Anomaly Visualizer
================================
macOS SIGSEGV fixes applied:
  1.  QtWebEngineWidgets MUST be imported BEFORE QApplication is created.
      On macOS the Chromium subprocess crashes the process when the import
      happens after QApplication.__init__.  We import it at the top of the
      module (before any Qt object is instantiated).

  2.  QApplication must receive sys.argv, not [].  On macOS an empty argv
      causes a NULL-dereference inside the Cocoa platform plugin.

  3.  sys.argv must be extended with the high-DPI / WebEngine flags BEFORE
      QApplication() is called, not after.

  4.  QWebEngineView.load() requires a QUrl built with
      QUrl.fromLocalFile(abs_path).  Passing a plain string is silently
      ignored on some builds and crashes on others.

  5.  The Chromium sandbox on macOS ARM (Apple Silicon) requires
      QTWEBENGINE_DISABLE_SANDBOX=1 when running under certain Python
      virtual-environment paths that lack the helper binary.

  6.  Font-family warning fix: use 'Courier New' explicitly instead of the
      generic alias 'Monospace' which Qt cannot resolve on macOS.
"""

# ── CRITICAL: WebEngine import BEFORE QApplication ────────────────────────────
import os
import sys

# Must set env vars before any Qt import
os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")        # fix #5
os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS",
                      "--disable-gpu --disable-software-rasterizer")

# Must extend argv before QApplication is constructed               fix #3
if "--no-sandbox" not in sys.argv:
    sys.argv += ["--no-sandbox"]

# WebEngine import FIRST — before QApplication                      fix #1
from PyQt5.QtWebEngineWidgets import QWebEngineView                # noqa: E402

import tempfile
import pandas as pd
import numpy as np
from pathlib import Path
import folium
from folium import plugins
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QTabWidget, QTextEdit,
    QFileDialog, QMessageBox, QProgressBar, QTableWidget, QTableWidgetItem,
    QGroupBox, QFormLayout, QDoubleSpinBox, QCheckBox,
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QUrl
from PyQt5.QtGui import QFont, QColor


# ── Palette ────────────────────────────────────────────────────────────────────
#   #000000  jet black    → app background, deep surfaces
#   #9999A1  ash grey     → borders, secondary text, button fill
#   #E6E6E9  pale silver  → primary text, inputs, highlights

STYLESHEET = """
QMainWindow, QWidget {
    background-color: #000000;
    color: #E6E6E9;
    font-family: 'Courier New', Courier, monospace;
    font-size: 12px;
}
QGroupBox {
    background-color: #0D0D0D;
    border: 1px solid #9999A1;
    border-radius: 0px;
    margin-top: 20px;
    padding: 10px 8px 8px 8px;
    color: #9999A1;
    font-size: 10px;
    letter-spacing: 2px;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 8px;
    background-color: #000000;
    color: #9999A1;
    font-size: 9px;
    letter-spacing: 3px;
}
QLabel {
    color: #E6E6E9;
    background: transparent;
}
QComboBox {
    background-color: #0D0D0D;
    border: 1px solid #9999A1;
    color: #E6E6E9;
    padding: 4px 8px;
    min-height: 26px;
    font-family: 'Courier New', Courier, monospace;
    border-radius: 0px;
}
QComboBox::drop-down { border: none; width: 20px; }
QComboBox::down-arrow {
    border-left: 2px solid #9999A1;
    border-bottom: 2px solid #9999A1;
    width: 6px; height: 6px;
    margin-right: 6px;
}
QComboBox QAbstractItemView {
    background-color: #0D0D0D;
    border: 1px solid #9999A1;
    color: #E6E6E9;
    selection-background-color: #9999A1;
    selection-color: #000000;
    outline: none;
}
QDoubleSpinBox, QSpinBox {
    background-color: #0D0D0D;
    border: 1px solid #9999A1;
    color: #E6E6E9;
    padding: 4px 8px;
    min-height: 26px;
    font-family: 'Courier New', Courier, monospace;
    border-radius: 0px;
}
QDoubleSpinBox::up-button, QSpinBox::up-button,
QDoubleSpinBox::down-button, QSpinBox::down-button {
    background-color: #1A1A1A;
    border: none;
    width: 16px;
}
QPushButton {
    background-color: #9999A1;
    color: #000000;
    border: none;
    padding: 9px 14px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1.5px;
    min-height: 32px;
    border-radius: 0px;
}
QPushButton:hover    { background-color: #E6E6E9; color: #000000; }
QPushButton:pressed  { background-color: #6A6A72; color: #E6E6E9; }
QPushButton:disabled { background-color: #1E1E1E; color: #444448; border: 1px solid #333338; }
QCheckBox {
    color: #E6E6E9;
    spacing: 8px;
    font-family: 'Courier New', Courier, monospace;
}
QCheckBox::indicator {
    width: 13px; height: 13px;
    border: 1px solid #9999A1;
    background-color: #0D0D0D;
}
QCheckBox::indicator:checked { background-color: #9999A1; }
QCheckBox::indicator:hover   { border-color: #E6E6E9; }
QTextEdit {
    background-color: #0D0D0D;
    border: 1px solid #9999A1;
    color: #E6E6E9;
    font-family: 'Courier New', Courier, monospace;
    font-size: 11px;
    padding: 6px;
    selection-background-color: #9999A1;
    selection-color: #000000;
    border-radius: 0px;
}
QTabWidget::pane { border: 1px solid #9999A1; background-color: #000000; }
QTabBar::tab {
    background-color: #000000;
    color: #9999A1;
    border: 1px solid #9999A1;
    border-bottom: none;
    padding: 7px 20px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 10px;
    letter-spacing: 2px;
    min-width: 80px;
}
QTabBar::tab:selected       { background-color: #9999A1; color: #000000; font-weight: bold; }
QTabBar::tab:hover:!selected { background-color: #1A1A1A; color: #E6E6E9; }
QTableWidget {
    background-color: #0D0D0D;
    border: 1px solid #9999A1;
    gridline-color: #1E1E1E;
    color: #E6E6E9;
    font-family: 'Courier New', Courier, monospace;
    font-size: 11px;
    selection-background-color: #9999A1;
    selection-color: #000000;
}
QHeaderView::section {
    background-color: #9999A1;
    color: #000000;
    border: none;
    padding: 6px 8px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 10px;
    letter-spacing: 1px;
    font-weight: bold;
}
QTableWidget::item          { padding: 4px 8px; border-bottom: 1px solid #1A1A1A; }
QTableWidget::item:selected { background-color: #9999A1; color: #000000; }
QProgressBar {
    border: 1px solid #9999A1;
    background-color: #0D0D0D;
    color: #E6E6E9;
    text-align: center;
    font-family: 'Courier New', Courier, monospace;
    height: 12px;
    border-radius: 0px;
}
QProgressBar::chunk { background-color: #9999A1; }
QScrollBar:vertical            { border: none; background: #000000; width: 8px; }
QScrollBar:horizontal          { border: none; background: #000000; height: 8px; }
QScrollBar::handle:vertical    { background: #9999A1; min-height: 20px; }
QScrollBar::handle:horizontal  { background: #9999A1; min-width:  20px; }
QScrollBar::add-line:vertical,  QScrollBar::sub-line:vertical   { height: 0px; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width:  0px; }
QMessageBox, QFileDialog       { background-color: #000000; color: #E6E6E9; }
QMessageBox QLabel             { color: #E6E6E9; font-family: 'Courier New', Courier, monospace; }
"""


# ── Worker Thread ──────────────────────────────────────────────────────────────

class AnomalyDetectionWorker(QThread):
    progress_update = pyqtSignal(str)
    finished        = pyqtSignal(dict)
    error           = pyqtSignal(str)

    def __init__(self, X_scaled, coords, model_type, nu_contamination):
        super().__init__()
        self.X_scaled         = X_scaled
        self.coords           = coords
        self.model_type       = model_type
        self.nu_contamination = nu_contamination

    def run(self):
        try:
            self.progress_update.emit(
                f"[RUN]  {self.model_type}  (contamination={self.nu_contamination:.3f})"
            )

            # sklearn needs ndarray, not DataFrame
            X = (self.X_scaled.values
                 if isinstance(self.X_scaled, pd.DataFrame)
                 else np.asarray(self.X_scaled))

            if self.model_type == "One-Class SVM":
                model = OneClassSVM(kernel="rbf", gamma="scale",
                                    nu=self.nu_contamination)
            else:
                model = IsolationForest(n_estimators=200,
                                        contamination=self.nu_contamination,
                                        random_state=42)

            model.fit(X)
            preds = model.predict(X)
            self.progress_update.emit("[OK]   Prediction complete — assembling results…")

            results = self.coords.copy().reset_index(drop=True)
            results[f"{self.model_type}_Label"]   = preds
            results[f"{self.model_type}_Anomaly"] = (preds == -1)
            anomalies = results[results[f"{self.model_type}_Anomaly"]].copy()

            self.finished.emit({
                "model_type":         self.model_type,
                "results":            results,
                "anomalies":          anomalies,
                "total_samples":      len(results),
                "anomaly_count":      len(anomalies),
                "anomaly_percentage": (len(anomalies) / len(results) * 100)
                                       if len(results) else 0.0,
            })

        except Exception as exc:
            self.error.emit(str(exc))


# ── Main Window ────────────────────────────────────────────────────────────────

class HeavyMetalsAnomalyVisualizer(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heavy Metals Anomaly Visualizer")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(900, 600)

        self.X_scaled   = None
        self.coords     = None
        self.results    = None
        self.anomalies  = None
        self.model_type = None
        self._map_tmp   = None

        self.setStyleSheet(STYLESHEET)
        self._init_ui()
        self._load_data()

    # ── UI ─────────────────────────────────────────────────────────────────────

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setSpacing(12)
        root.setContentsMargins(12, 12, 12, 12)
        root.addWidget(self._build_control_panel(), stretch=1)
        root.addWidget(self._build_display_panel(),  stretch=2)

    def _build_control_panel(self):
        group  = QGroupBox("Detection Controls")
        layout = QVBoxLayout()
        layout.setSpacing(10)

        title = QLabel("HEAVY METALS\nANOMALY VISUALIZER")
        font  = QFont("Courier New", 13)
        font.setBold(True)
        title.setFont(font)
        title.setStyleSheet(
            "color:#E6E6E9; letter-spacing:2px; padding-bottom:2px;"
        )
        layout.addWidget(title)

        rule = QLabel()
        rule.setFixedHeight(1)
        rule.setStyleSheet("background:#9999A1; margin-bottom:4px;")
        layout.addWidget(rule)

        # Model params ─────────────────────────────────────────────────────────
        mdl_box    = QGroupBox("Model")
        mdl_layout = QFormLayout()
        mdl_layout.setSpacing(8)

        self.model_combo = QComboBox()
        self.model_combo.addItems(["One-Class SVM", "Isolation Forest"])
        mdl_layout.addRow("Algorithm :", self.model_combo)

        self.nu_spinbox = QDoubleSpinBox()
        self.nu_spinbox.setRange(0.01, 0.50)
        self.nu_spinbox.setValue(0.05)
        self.nu_spinbox.setSingleStep(0.01)
        self.nu_spinbox.setDecimals(3)
        self.nu_spinbox.setToolTip(
            "Expected fraction of anomalies in the dataset"
        )
        mdl_layout.addRow("Contamination :", self.nu_spinbox)
        mdl_box.setLayout(mdl_layout)
        layout.addWidget(mdl_box)

        # Run + progress ───────────────────────────────────────────────────────
        self.run_button = QPushButton("▶  RUN DETECTION")
        self.run_button.clicked.connect(self._run_detection)
        layout.addWidget(self.run_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)   # indeterminate spinner
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Map layer toggles ────────────────────────────────────────────────────
        viz_box    = QGroupBox("Map Layers")
        viz_layout = QVBoxLayout()
        viz_layout.setSpacing(6)
        self.heat_checkbox    = QCheckBox("Heatmap overlay")
        self.heat_checkbox.setChecked(True)
        self.cluster_checkbox = QCheckBox("Cluster markers")
        self.cluster_checkbox.setChecked(True)
        viz_layout.addWidget(self.heat_checkbox)
        viz_layout.addWidget(self.cluster_checkbox)
        viz_box.setLayout(viz_layout)
        layout.addWidget(viz_box)

        # Action buttons ───────────────────────────────────────────────────────
        self.viz_button = QPushButton("◈  GENERATE MAP")
        self.viz_button.clicked.connect(self._generate_map)
        self.viz_button.setEnabled(False)
        layout.addWidget(self.viz_button)

        self.export_button = QPushButton("⬇  EXPORT ANOMALIES CSV")
        self.export_button.clicked.connect(self._export_anomalies)
        self.export_button.setEnabled(False)
        layout.addWidget(self.export_button)

        # Status log ───────────────────────────────────────────────────────────
        log_box    = QGroupBox("Status Log")
        log_layout = QVBoxLayout()
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setFixedHeight(200)
        log_layout.addWidget(self.results_text)
        log_box.setLayout(log_layout)
        layout.addWidget(log_box)

        layout.addStretch()
        group.setLayout(layout)
        return group

    def _build_display_panel(self):
        tabs = QTabWidget()
        tabs.setDocumentMode(True)

        self.map_view = QWebEngineView()
        self.map_view.setMinimumHeight(400)
        tabs.addTab(self.map_view, "MAP")

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(
            ["#", "Longitude (X)", "Latitude (Y)", "Model", "Status"]
        )
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.verticalHeader().setVisible(False)
        tabs.addTab(self.results_table, "RESULTS TABLE")

        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        tabs.addTab(self.stats_text, "STATISTICS")

        return tabs

    # ── Data loading ───────────────────────────────────────────────────────────

    def _load_data(self):
        try:
            repo_path     = Path(__file__).parent
            x_scaled_path = repo_path / "X_scaled_features.csv"
            coords_path   = repo_path / "coords.csv"

            if x_scaled_path.exists() and coords_path.exists():
                self.X_scaled = pd.read_csv(x_scaled_path)
                self.coords   = pd.read_csv(coords_path)
                self._log(
                    f"[OK]  Data loaded.\n"
                    f"      Samples  : {len(self.X_scaled):,}\n"
                    f"      Features : {list(self.X_scaled.columns)}"
                )
            else:
                missing = [p for p in (x_scaled_path, coords_path)
                           if not p.exists()]
                self._log(
                    "[WARN] File(s) not found:\n"
                    + "".join(f"       - {p.name}\n" for p in missing)
                    + "       Run preprocessing.ipynb first."
                )
        except Exception as exc:
            self._log(f"[ERR]  Data load failed: {exc}")

    # ── Detection ──────────────────────────────────────────────────────────────

    def _run_detection(self):
        if self.X_scaled is None or self.coords is None:
            QMessageBox.critical(
                self, "No Data",
                "Data not loaded.\nRun preprocessing.ipynb first."
            )
            return

        self.run_button.setEnabled(False)
        self.viz_button.setEnabled(False)
        self.export_button.setEnabled(False)
        self.progress_bar.setVisible(True)

        self.worker = AnomalyDetectionWorker(
            self.X_scaled,
            self.coords,
            self.model_combo.currentText(),
            self.nu_spinbox.value(),
        )
        self.worker.progress_update.connect(self._log)
        self.worker.finished.connect(self._on_detection_finished)
        self.worker.error.connect(self._on_worker_error)
        self.worker.start()

    def _on_detection_finished(self, output):
        self.model_type = output["model_type"]
        self.results    = output["results"]
        self.anomalies  = output["anomalies"]

        self.progress_bar.setVisible(False)
        self.run_button.setEnabled(True)
        self.viz_button.setEnabled(True)
        self.export_button.setEnabled(True)

        self._log(
            f"[DONE] {self.model_type}\n"
            f"       Total     : {output['total_samples']:,}\n"
            f"       Anomalies : {output['anomaly_count']:,}\n"
            f"       Rate      : {output['anomaly_percentage']:.2f}%"
        )
        self._populate_table()
        self._populate_stats()

    def _on_worker_error(self, msg):
        self.progress_bar.setVisible(False)
        self.run_button.setEnabled(True)
        self._log(f"[ERR]  {msg}")
        QMessageBox.critical(self, "Detection Error", msg)

    # ── Table ──────────────────────────────────────────────────────────────────

    def _populate_table(self):
        self.results_table.setRowCount(0)
        if self.anomalies is None or self.anomalies.empty:
            return

        for display_i, (orig_i, row) in enumerate(
            self.anomalies.head(100).iterrows()
        ):
            self.results_table.insertRow(display_i)
            cells = [
                str(orig_i),
                f"{row['X']:.6f}",
                f"{row['Y']:.6f}",
                self.model_type,
                "ANOMALY",
            ]
            for col, text in enumerate(cells):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                if col == 4:
                    item.setForeground(QColor("#9999A1"))
                    item.setFont(QFont("Courier New", 10, QFont.Bold))
                self.results_table.setItem(display_i, col, item)

        self.results_table.resizeColumnsToContents()

    # ── Statistics ─────────────────────────────────────────────────────────────

    def _populate_stats(self):
        if self.results is None or self.anomalies is None:
            return

        total  = len(self.results)
        n_anom = len(self.anomalies)
        rate   = (n_anom / total * 100) if total else 0
        ax, ay = self.anomalies["X"], self.anomalies["Y"]

        self.stats_text.setText(
            "=" * 46 + "\n"
            "  STATISTICAL SUMMARY\n"
            + "=" * 46 + "\n\n"
            f"  Model         : {self.model_type}\n"
            f"  Total samples : {total:,}\n"
            f"  Anomalies     : {n_anom:,}\n"
            f"  Normal        : {total - n_anom:,}\n"
            f"  Rate          : {rate:.4f}%\n\n"
            + "-" * 46 + "\n"
            "  GEOGRAPHIC DISTRIBUTION  (anomalies)\n"
            + "-" * 46 + "\n"
            f"  Longitude (X)\n"
            f"    Min  : {ax.min():.6f}\n"
            f"    Max  : {ax.max():.6f}\n"
            f"    Mean : {ax.mean():.6f}\n"
            f"    Std  : {ax.std():.6f}\n\n"
            f"  Latitude (Y)\n"
            f"    Min  : {ay.min():.6f}\n"
            f"    Max  : {ay.max():.6f}\n"
            f"    Mean : {ay.mean():.6f}\n"
            f"    Std  : {ay.std():.6f}\n"
            + "=" * 46 + "\n"
        )

    # ── Map ────────────────────────────────────────────────────────────────────

    def _generate_map(self):
        if self.anomalies is None or self.coords is None:
            QMessageBox.warning(self, "Warning", "Run detection first.")
            return

        try:
            center = [
                float(self.coords["Y"].mean()),
                float(self.coords["X"].mean()),
            ]
            m = folium.Map(location=center, zoom_start=8,
                           tiles="OpenStreetMap")

            # All sample points — ash grey
            for _, row in self.coords.iterrows():
                folium.CircleMarker(
                    location=[float(row["Y"]), float(row["X"])],
                    radius=3,
                    popup="Sample",
                    color="#9999A1",
                    fill=True,
                    fill_color="#9999A1",
                    fill_opacity=0.45,
                    weight=1,
                ).add_to(m)

            # Anomaly points — black fill / silver ring
            for idx, row in self.anomalies.iterrows():
                folium.CircleMarker(
                    location=[float(row["Y"]), float(row["X"])],
                    radius=7,
                    popup=folium.Popup(f"Anomaly #{idx}", parse_html=True),
                    color="#E6E6E9",
                    fill=True,
                    fill_color="#000000",
                    fill_opacity=0.9,
                    weight=2,
                ).add_to(m)

            if self.heat_checkbox.isChecked() and not self.anomalies.empty:
                heat_data = [
                    [float(r["Y"]), float(r["X"])]
                    for _, r in self.anomalies.iterrows()
                ]
                plugins.HeatMap(
                    heat_data, radius=15, blur=25, max_zoom=1
                ).add_to(m)

            if self.cluster_checkbox.isChecked() and not self.anomalies.empty:
                from folium.plugins import MarkerCluster
                mc = MarkerCluster()
                for idx, row in self.anomalies.iterrows():
                    folium.Marker(
                        location=[float(row["Y"]), float(row["X"])],
                        popup=f"Anomaly {idx}",
                        icon=folium.Icon(color="black",
                                         icon="exclamation-sign"),
                    ).add_to(mc)
                mc.add_to(m)

            # Save to a temp file then load via proper QUrl  (fix #4)
            tmp = tempfile.NamedTemporaryFile(
                delete=False, suffix=".html", mode="w", encoding="utf-8"
            )
            m.save(tmp.name)
            tmp.close()
            self._map_tmp = tmp.name

            url = QUrl.fromLocalFile(os.path.abspath(self._map_tmp))
            self.map_view.load(url)
            self._log("[MAP]  Map generated and loaded.")

        except Exception as exc:
            QMessageBox.critical(self, "Map Error",
                                 f"Failed to generate map:\n{exc}")
            self._log(f"[ERR]  Map failed: {exc}")

    # ── Export ─────────────────────────────────────────────────────────────────

    def _export_anomalies(self):
        if self.anomalies is None or self.anomalies.empty:
            QMessageBox.warning(self, "Warning", "No anomalies to export.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Save Anomalies", "anomalies.csv", "CSV Files (*.csv)"
        )
        if path:
            try:
                self.anomalies.to_csv(
                    path, index=True, index_label="original_index"
                )
                QMessageBox.information(
                    self, "Exported",
                    f"Saved {len(self.anomalies):,} rows to:\n{path}",
                )
                self._log(
                    f"[CSV]  Exported {len(self.anomalies):,} rows → {path}"
                )
            except Exception as exc:
                QMessageBox.critical(self, "Export Error", str(exc))
                self._log(f"[ERR]  Export failed: {exc}")

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _log(self, msg: str) -> None:
        self.results_text.append(msg)
        sb = self.results_text.verticalScrollBar()
        sb.setValue(sb.maximum())


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    # fix #2 — always pass the real sys.argv list
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = HeavyMetalsAnomalyVisualizer()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

    