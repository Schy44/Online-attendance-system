import requests

def fetch_image_from_esp32(esp32_ip):

    # Fetches a captured JPEG image from the ESP32 CameraWebServer.
    
    # Build the URL for the image capture endpoint.
    url = f"http://{esp32_ip}/capture"
    print(f"Fetching image from {url} ...")
    
    try:
        # Send an HTTP GET request to the ESP32.
        response = requests.get(url)
        response.raise_for_status()  
        
        # Save the image content to a local file.
        image_filename = "captured_image.jpg"
        with open(image_filename, "wb") as file:
            file.write(response.content)
        print(f"Image successfully saved as {image_filename}")
        return image_filename
    
    except requests.RequestException as e:
        # Handle exceptions from the requests library.
        print(f"Error fetching image from ESP32: {e}")
        return None

def main():
    esp32_ip = input("Enter your ESP32 IP address (default 192.168.0.106): ").strip() or "192.168.0.106"
    fetch_image_from_esp32(esp32_ip)

if __name__ == "__main__":
    # Prompt the user to enter the ESP32 IP address.
    
    esp32_ip = input("Enter your ESP32 IP address (default 192.168.0.106): ").strip() or "192.168.0.106"
    fetch_image_from_esp32(esp32_ip)
