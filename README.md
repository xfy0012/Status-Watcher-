# Status-Watcher

## Architecture Overview

```mermaid
graph TD
    subgraph Front-end
        A[Front-end Page] -->|Add/Delete URL| B[Flask API]
        A -->|View Status| B
        B -->|Return Data| A
    end

    subgraph Backend
        B -->|Save Data| C[(Database)]
        D[Scheduled Task] -->|Read URL List| C
        D -->|Check Status| E{Website Status}
        E -->|Up| D
        E -->|Down/Recovered| F[Notification Module]
        F -->|Send Alert| G[User]
        E -->|Log Result| C
    end
