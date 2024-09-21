import { useState, useEffect } from "react";
import axios from 'axios';

export default function QR() {

  const [qrImage, setQrImage] = useState(null);

  useEffect(() => {


    const fetchImage = () => {
      axios.get('http://localhost:5000', { responseType: 'blob' } )
      .then(response => {
        const url = URL.createObjectURL(response.data);
        setQrImage(url);
      })
      .catch(error => {
        console.log('Error fetching QR code image:', error);
      });

      const intervalId = setInterval(fetchImage, 1000);

      return () => clearInterval(intervalId);  // Cleanup on component unmount
    }
  }, [])

  return (
    <div className="d-flex justify-content-center">
      {qrImage ? <img src={qrImage} alt="qr-code" /> : <p>No QR Image</p>}
    </div>
  )
}
