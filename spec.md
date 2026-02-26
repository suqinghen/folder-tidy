# Specification: Media Organizer LLM Agent

## 1. Project Overview
This project is an intelligent file organization tool powered by Large Language Models (LLMs). It scans directories containing messy collections of media files (Music, Movies, TV Series, E-books) and reorganizes them into a structured, canonical hierarchy.

## 2. Goals
- **Automate Organization**: Transform chaotic folders into a clean library structure with minimal user intervention.
- **Intelligent parsing**: Leverage LLMs to parse ambiguous filenames and retrieve metadata where traditional tools fail.
- **Multi-Media Support**: Handle Music, Movies, TV Series, and E-books with specialized handling for each.
- **Safety**: Provide a safe "dry-run" mechanism to review changes before application and ensure no data loss.

## 3. Core Features

### 3.1. Media Type Detection
- Heuristic and extension-based detection to categorize files into Music, Video (Movies/TV), or Text (E-books).
- LLM-based fallback for ambiguous files or when metadata is missing.

### 3.2. Metadata Extraction & Enrichment
- **Traditional Extraction**: Use libraries (e.g., `mutagen` for audio, `ffmpeg` for video, `ebooklib` for books) to read embedded tags.
- **LLM Agent**:
  - Analyzes the filename and context.
  - Fixes typos, identifies canonical titles, artists, years, and series information.
  - Distinguishes between similarly named content (e.g., Remakes, US/UK versions).
  - Fetches missing metadata (Year, Director, Author, Genre) via LLM knowledge or external APIs if integrated.

### 3.3. Organization & Renaming
- Configurable templates for folder structure and file naming.
  - **Music**: `Music/{Artist}/{Album} ({Year})/{Track} - {Title}.{ext}`
  - **Movies**: `Movies/{Title} ({Year})/{Title} ({Year}).{ext}`
  - **TV Series**: `TV Shows/{Series}/{Season XX}/{Series} - S{XX}E{YY} - {Episode Title}.{ext}`
  - **E-books**: `Books/{Author}/{Series}/{Index} - {Title}.{ext}`

### 3.4. Safety & Logging
- **Dry Run Mode**: Generate a report of proposed changes without modifying files.
- **Undo Functionality**: Maintain a transaction log to reverse operations if needed.
- **Duplicate Handling**: Detect duplicates (by content hash or metadata match) and propose deletion or archiving.

## 4. Architecture

### 4.1. System Components
1.  **Scanner**: Recursively traverses input paths, ignoring system files.
2.  **Classifier**: Determines the media type of each file based on extensions and initial inspection.
3.  **Analyzer (The Agent)**:
    - Constructs a prompt with file info.
    - Queries the LLM (OpenAI/Anthropic/Local).
    - Returns a structured metadata object (JSON).
4.  **Planner**: Maps metadata to the target path structure based on configuration.
5.  **Executor**: Performs file moves/renames (Atomic operations).
6.  **Reviewer (CLI/UI)**: Allows user to inspect the plan before execution.

### 4.2. Data Flow
`Input File` -> `Scanner` -> `Classifier` -> `Analyzer (LLM)` -> `Structured Metadata` -> `Planner` -> `Proposed Action` -> `User Approval` -> `Executor`

## 5. Technology Stack (Proposed)
- **Language**: Python 3.10+
- **LLM Integration**: `langchain` or direct API clients (OpenAI, Anthropic).
- **File Handling**: `shutil`, `pathlib`.
- **CLI**: `typer` or `click`.
- **Metadata Libraries**: `mutagen` (audio), `PyPDF2`/`EbookLib` (books), `ffmpeg-python` (video).
- **Configuration**: YAML or TOML.

## 6. Configuration
The system will use a `config.yaml` to define:
- **Input/Output directories**: Source paths to scan and destination library root.
- **Naming templates**: Custom format strings for file renaming.
- **API Keys**: Credentials for LLM providers.
- **LLM Model selection**: (e.g., `gpt-4o`, `claude-3-5-sonnet`, `llama3`).
- **Behavior**: Overwrite policies, trash handling, dry-run default.
