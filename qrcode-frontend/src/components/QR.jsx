import { useState, useEffect } from "react";

export default function QR() {

  const [qrImage, setQrImage] = useState(null);

  const fetchQRCode = async () => {
    try {
      // Fetch the QR code image from the Python server
      const response = await fetch('https://cors-anywhere.herokuapp.com/http://localhost:8000/qr_code.png');
      if (response.ok) {
        const imageBlob = await response.blob();
        const imageUrl = URL.createObjectURL(imageBlob);
        setQrImage(imageUrl);
      } else {
        console.error('Error fetching QR code:', response.statusText);
      }
    } catch (error) {
      console.error('Error fetching QR code:', error);
    }
  };
  

  useEffect(() => {
    // Poll every 2 seconds to get the latest QR code image
    const interval = setInterval(() => {
      fetchQRCode();
    }, 1000);
    return () => clearInterval(interval);  // Cleanup interval on unmount
  }, []);

  return (
    <div className="d-flex justify-content-center">
      {qrImage ? <img src={qrImage} alt="qr-code" /> : <p>No QR Image</p>}
    </div>
  )
}
