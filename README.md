# py-meari (Python, unofficial)

This project is an **unofficial Python reimplementation** of the [Meari SDK](https://github.com/Mearitek/MeariSdk).  
It aims to replicate the functionality of the original SDK to connect with the **meari platform** and manage **IP cameras** without relying on the official closed-source binaries.

⚠️ Disclaimer: This is a community-driven project. It is not affiliated with Mearitek or the official Meari SDK.

---

## Features

- Reverse-engineered communication with the meari platform  
- Authentication and session handling  
- Camera discovery and management  
- Command-Line Interface (CLI) for quick tests  
- Python SDK for integration into custom applications  

---

## Project Structure

```
meari-main/
│
├── meari_sdk/          # Core SDK reimplementation
├── cli.py              # Command-line entrypoint
├── const.py            # Constants and configuration values
├── requirements.txt    # Python dependencies
├── LICENSE             # License file
└── README.md           # Project documentation (this file)
```

---

## Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/wilds/meari.git
pip install -r requirements.txt
```

Requirements:
- Python 3.8+
- See `requirements.txt` for libraries

---

## Usage

### Command-Line Interface

The CLI provides quick access to SDK features:

```bash
python cli.py
```

### SDK in Python

You can use the SDK programmatically in your own scripts:

```python
from meari_sdk.meari_client import MeariClient

client = MeariClient(country_code=country_code, phone_code=phone_code, phone_type=phone_type, lng_type=lng_type, partner=KNOWN_PARTNERS[partner])
login_data = self.client.login(user_account.lower(), user_password)

# Example: list available cameras
cameras = client.get_device()
for cam in cameras:
    print(f"ID: {cam['id']})")
```

---


## Contributing

Contributions are welcome!  
If you discover new endpoints, features, or improvements to the SDK, please submit a pull request or open an issue.

---

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.  
Not affiliated with Mearitek or the official Meari SDK.
