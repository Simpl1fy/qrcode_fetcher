import { useState, useEffect } from "react";
import axios from 'axios'
import io from 'socket.io-client'

export default function QR() {

  const socket = io('http://localhost:5000',
    {
      transports: ['websocket', 'polling']
    }
  );

  const [qrImage, setQrImage] = useState(null);

  const fetchQRCode = async () => {
    try {
      console.log("Image is being requested");
      const response = await axios.get('http://localhost:5000/getimage', { responseType: 'blob' });
      const imageUri = URL.createObjectURL(response.data);
      setQrImage(imageUri);
    } catch(err) {
      console.error(err);
    }
  };
  

  useEffect(() => {

    

    // Handle connection events
    socket.on('connect', () => {
      console.log('Connected to the WebSocket server');
    });

    socket.on('qr_code_updated', (data) => {
      console.log('Image has been updated, fetching');
      console.log("Image update recieved", data)
      fetchQRCode();  // Fetch image when the event is triggered
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server');
    });

    socket.on('connect_error', (err) => {
      console.error('Connection Error:', err);
    });

    // Fetch the initial image
    fetchQRCode();

    // Cleanup function to disconnect WebSocket and remove event listeners
    return () => {
      socket.off('qr_code_updated'); // Remove the event listener
      socket.disconnect(); // Disconnect the WebSocket
    };
  }, []);

  return (
    <>
      <div className="d-flex justify-content-center">
        {qrImage ? <img src={qrImage} alt="qr-code" /> : <p>No QR Image</p>}
      </div>
    </>
  )
}
