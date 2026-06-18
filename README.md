# NodeExporter for Blender

[![Blender Version](https://img.shields.io/badge/Blender-4.2+-orange.svg)](https://www.blender.org)
[![License](https://img.shields.io/badge/License-GPL_3.0-blue.svg)](LICENSE)

<img width="1920" height="1080" alt="NODE EXPORTER PROJECT 1" src="https://github.com/user-attachments/assets/5d3afe25-ee88-4840-9e02-6486bae9fb72" />

NodeExporter is a Blender add-on designed to extract node networks (Geometry Nodes and Shader Materials) and compile them into an interactive and independent web viewer based on HTML5, CSS3, and JavaScript.

The purpose of this tool is to facilitate the visualization, documentation, and graphical export of complex node systems outside the Blender environment, maintaining high visual and operational fidelity.

## Key Features

<img width="1920" height="1080" alt="NODE EXPORTER PROJECT 2" src="https://github.com/user-attachments/assets/6f099712-29a4-4e10-9785-17294282f280" />

* **Standalone Web Viewer:** Generates a standalone HTML file that does not require local servers or external dependencies to run.
* **High-Resolution Image Export:** Enables exporting the web canvas to PNG format (2x scale), supporting solid backgrounds or alpha channel (transparency) for integration into graphic composition and editing software.
* **Dynamic Interface and Canvas:** Implements an infinite and resizable workspace, with an overlay interface that allows real-time customization of the background, grid density, and connection routing (thickness and line style).
* **Native State Synchronization:** Detects and reproduces the state of elements from Blender, supporting minimized (collapsed) nodes and individual socket hiding, automatically readjusting link topology.
* **Interactive Operations:** Allows network modification directly in the browser, including block repositioning, link disconnection, and frame management via a context menu.

## Installation

1. Download the `NodeExporter.zip` file from the **Releases** section of this repository.
2. In Blender, go to **Edit > Preferences > Get Extensions** (or Add-ons).
3. Click the drop-down menu and choose **Install from Disk...** (or Install...), select the downloaded `NodeExporter.zip` file, and confirm.
4. Check the box corresponding to **NodeExporter** in the extensions list.
5. The control panel will be available in the sidebar (`N` key) of the Node Editor.

## Usage Instructions

1. Open a workspace in Blender containing an active Geometry Nodes tree or Material.
2. Open the sidebar in the Node Editor and locate the **NodeExporter** tab.
3. Click the **Use Active Node Tree** button to set the active node tree as the export target.
4. Select the destination directory on your local system.
5. Click **Export and Open Viewer**. The system will generate the JSON data file, compile the HTML file, and execute it in your default web browser.

<img width="397" height="510" alt="Captura de pantalla 2026-06-18 125127" src="https://github.com/user-attachments/assets/c3da4537-2039-4388-9908-26ff86524947" />
<img width="402" height="527" alt="Captura de pantalla 2026-06-18 125135" src="https://github.com/user-attachments/assets/db71b39c-769a-4c22-9515-d31022e3978a" />

## Showcase Video

https://github.com/user-attachments/assets/0731de55-1a80-49c8-b755-2b51091aa429

## Project Architecture

The add-on is structured into three main components:

```text
NodeExporter/
├── __init__.py           # Backend logic: Extraction via Blender API and JSON data formatting.
├── visor.html            # Frontend engine: DOM rendering, canvas calculations, and interactive UI.
└── blender_manifest.toml # Extension metadata for the official Blender platform.
