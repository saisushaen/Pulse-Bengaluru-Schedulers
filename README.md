# Pulse Bengaluru Schedulers

This repository contains three independent Python schedulers, each designed to perform specific tasks related to data processing and messaging within the Google Cloud Platform (GCP) ecosystem.

## Technologies Used

Each scheduler utilizes the following core Python libraries:

- **pandas**: For data manipulation and analysis.
- **google-cloud-storage**: For interacting with Google Cloud Storage.
- **google-cloud-pubsub**: For interacting with Google Cloud Pub/Sub.

## Project Structure

The project is organized into separate directories for each scheduler:

```
Pulse Bengaluru Schedulers/
├── Scheduler-1/
│   ├── main.py
│   └── requirements.txt
├── Scheduler-2/
│   ├── main.py
│   └── requirements.txt
└── Scheduler-3/
    ├── main.py
    └── requirements.txt
```

## Getting Started

To run these schedulers locally, follow these steps:

### Prerequisites

- Python 3.x installed.
- Google Cloud SDK configured and authenticated with access to the necessary GCP resources (Cloud Storage, Pub/Sub).

### Local Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/Pulse-Bengaluru-Schedulers.git
    cd Pulse-Bengaluru-Schedulers
    ```

2.  **Install dependencies for each scheduler:**

    Navigate into each scheduler's directory and install its dependencies. Repeat for `Scheduler-2` and `Scheduler-3`.

    ```bash
    cd Scheduler-1
    pip install -r requirements.txt
    cd ..
    ```

### Running the Schedulers

Each `main.py` file can be executed independently. Ensure you are in the respective scheduler's directory.

```bash
# To run Scheduler-1
cd Scheduler-1
python main.py
cd ..

# To run Scheduler-2
cd Scheduler-2
python main.py
cd ..

# To run Scheduler-3
cd Scheduler-3
python main.py
cd ..
```

## Configuration

Each `main.py` file likely contains specific configurations (e.g., GCP project IDs, bucket names, Pub/Sub topic/subscription names). You may need to modify these files according to your GCP environment and requirements. Review the `main.py` files within each `Scheduler-X` directory for details.
