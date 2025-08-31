// 当且仅当 Onload 之后加载
// 按下按钮之后,挂载 Motion 和 Orientation
document.addEventListener('DOMContentLoaded', () => {
    // 获得显示区Element
    const body = document.getElementById('body');

    const accelXElem = document.getElementById('accelX');
    const accelYElem = document.getElementById('accelY');
    const accelZElem = document.getElementById('accelZ');

    const gyroAlphaElem = document.getElementById('gyroAlpha');
    const gyroBetaElem = document.getElementById('gyroBeta');
    const gyroGammaElem = document.getElementById('gyroGamma');

    const statusElem = document.getElementById('status');
    const startButton = document.getElementById('startSensors');

    // let motionListenerActive = false;
    // let orientationListenerActive = false;

    // --- WebSocket ---
    let socket;
    const wsUrl = 'wss://' + location.host + '/ws'; // Or your server's IP if not running on the same machine
    // e.g., 'ws://192.168.1.100:8765'
    // IMPORTANT: If your Python server is on "0.0.0.0",
    // use the actual IP address of the machine running the server
    // when accessing from another device (like your phone).
    // If both server and browser are on the same machine, 'localhost' is fine.
    function connectWebSocket() {
        if (socket && (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING)) {
            console.log("WebSocket is already open or connecting.");
            return;
        }

        socket = new WebSocket(wsUrl);

        socket.onopen = () => {
            console.log('WebSocket connection established.');
            if (statusElem) statusElem.textContent = '传感器已激活，WebSocket已连接。';
        };

        socket.onmessage = (event) => {
            console.log('Message from server:', event.data);
            // Handle messages from server if needed (e.g., acknowledgements)
        };

        socket.onclose = (event) => {
            console.log('WebSocket connection closed:', event.code, event.reason);
            if (statusElem) statusElem.textContent = 'WebSocket 连接已断开。尝试重新连接...';
            // Optional: attempt to reconnect after a delay
            setTimeout(connectWebSocket, 500);
        };

        socket.onerror = (error) => {
            console.error('WebSocket error:', error);
            if (statusElem) statusElem.textContent = 'WebSocket 连接错误。';
        };
    }
    // --- End WebSocket ---



    let currentAccel = { x: null, y: null, z: null };
    let currentGyro = { alpha: null, beta: null, gamma: null };

    function sendSensorData() {
        if (socket && socket.readyState === WebSocket.OPEN) {
            const dataToSend = {
                ...currentAccel,
                ...currentGyro
            };
            // Only send if we have some data
            if (Object.values(dataToSend).some(val => val !== null)) {
                socket.send(JSON.stringify(dataToSend));
            }
        }
    }

    function sendMessage() {
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({
                message: 'left',
            }));
        }
    }

    function handleMotion(event) {
        // if (!accelXElem || !accelYElem || !accelZElem) {
        // sendSensorData();
        // return;
        // }
        // if (!motionListenerActive) {
        //     statusElem.textContent = '加速度计数据已激活!';
        //     motionListenerActive = true;
        // }
        if (event.accelerationIncludingGravity) {
            if (accelXElem) accelXElem.textContent = event.accelerationIncludingGravity.x !== null ? event.accelerationIncludingGravity.x.toFixed(2) : 'N/A';
            if (accelYElem) accelYElem.textContent = event.accelerationIncludingGravity.y !== null ? event.accelerationIncludingGravity.y.toFixed(2) : 'N/A';
            if (accelZElem) accelZElem.textContent = event.accelerationIncludingGravity.z !== null ? event.accelerationIncludingGravity.z.toFixed(2) : 'N/A';
            currentAccel = {
                x: event.accelerationIncludingGravity.x,
                y: event.accelerationIncludingGravity.y,
                z: event.accelerationIncludingGravity.z
            };
        } else if (event.acceleration) { // Fallback for some devices
            if (accelXElem) accelXElem.textContent = event.acceleration.x !== null ? event.acceleration.x.toFixed(2) : 'N/A';
            if (accelYElem) accelYElem.textContent = event.acceleration.y !== null ? event.acceleration.y.toFixed(2) : 'N/A';
            if (accelZElem) accelZElem.textContent = event.acceleration.z !== null ? event.acceleration.z.toFixed(2) : 'N/A';
            currentAccel = {
                x: event.acceleration.x,
                y: event.acceleration.y,
                z: event.acceleration.z
            };
        } else {
            if (accelXElem) accelXElem.textContent = 'N/A';
            if (accelYElem) accelYElem.textContent = 'N/A';
            if (accelZElem) accelZElem.textContent = 'N/A';
        }

        sendSensorData();
    }

    function handleOrientation(event) {
        // if (!gyroAlphaElem || !gyroBetaElem || !gyroGammaElem) {
        //     sendSensorData();
        //     return;
        // }
        // if (!orientationListenerActive) {
        //     statusElem.textContent = '陀螺仪数据已激活!'; // This might overwrite accel status
        //     orientationListenerActive = true;
        // }
        if (gyroAlphaElem) gyroAlphaElem.textContent = event.alpha !== null ? event.alpha.toFixed(2) : 'N/A';
        if (gyroBetaElem) gyroBetaElem.textContent = event.beta !== null ? event.beta.toFixed(2) : 'N/A';
        if (gyroGammaElem) gyroGammaElem.textContent = event.gamma !== null ? event.gamma.toFixed(2) : 'N/A';

        currentGyro = {
            alpha: event.alpha,
            beta: event.beta,
            gamma: event.gamma,
        };

        sendSensorData();
    }

    function requestSensorPermissions() {
        connectWebSocket(); // Ensure WebSocket is connected before requesting permissions
        // Update status to indicate permission request 

        if (body) {

            return
        }

        if (statusElem) statusElem.textContent = '正在请求传感器权限...';

        // iOS 13+ Safari specific permission request
        if (typeof DeviceMotionEvent !== 'undefined' && typeof DeviceMotionEvent.requestPermission === 'function') {
            DeviceMotionEvent.requestPermission()
                .then(permissionState => {
                    if (permissionState === 'granted') {
                        window.addEventListener('devicemotion', handleMotion, true);
                        if (statusElem) statusElem.textContent = '加速度计权限已授予。';
                    } else {
                        if (statusElem) statusElem.textContent = '加速度计权限被拒绝。';
                    }
                })
                .catch(error => {
                    if (statusElem) statusElem.textContent = '请求加速度计权限时出错: ' + error;
                    console.error('DeviceMotionEvent Error:', error);
                });
        } else {
            // For other browsers or older iOS
            if (window.DeviceMotionEvent) {
                window.addEventListener('devicemotion', handleMotion, true);
                if (statusElem) statusElem.textContent = '尝试监听加速度计... (非iOS13+或安卓)';
            } else {
                if (statusElem) statusElem.textContent = '此浏览器不支持加速度计事件。';
            }
        }

        if (typeof DeviceOrientationEvent !== 'undefined' && typeof DeviceOrientationEvent.requestPermission === 'function') {
            DeviceOrientationEvent.requestPermission()
                .then(permissionState => {
                    if (permissionState === 'granted') {
                        window.addEventListener('deviceorientation', handleOrientation, true);
                        // Append to status, don't overwrite if motion was successful
                        if (statusElem) statusElem.textContent += ' 陀螺仪权限已授予。';
                    } else {
                        if (statusElem) statusElem.textContent += ' 陀螺仪权限被拒绝。';
                    }
                })
                .catch(error => {
                    if (statusElem) statusElem.textContent += ' 请求陀螺仪权限时出错: ' + error;
                    console.error('DeviceOrientationEvent Error:', error);
                });
        } else {
            // For other browsers or older iOS
            if (window.DeviceOrientationEvent) {
                window.addEventListener('deviceorientation', handleOrientation, true);
                if (statusElem) statusElem.textContent += ' 尝试监听陀螺仪... (非iOS13+或安卓)';
            } else {
                if (statusElem) statusElem.textContent += ' 此浏览器不支持陀螺仪事件。';
            }
        }

        // Hide the button after attempting to start
        if (startButton) startButton.style.display = 'none';
    }


    if (body) {
        body.addEventListener('click', sendMessage)
    }

    if (startButton) {
        startButton.addEventListener('click', requestSensorPermissions);
    } else {
        console.error("Start button not found!");
        requestSensorPermissions();
    }

    // Check if sensors are readily available (e.g., on Android or already permitted)
    // This is more of a fallback / immediate check if button isn't needed.
    // However, best practice is to always require user interaction for permission.
    if (!startButton) { // If there's no button, try to initialize directly (less common)
        console.error("Start button not found!");
        if (window.DeviceMotionEvent && !DeviceMotionEvent.requestPermission) {
            window.addEventListener('devicemotion', handleMotion);
        }
        if (window.DeviceOrientationEvent && !DeviceOrientationEvent.requestPermission) {
            window.addEventListener('deviceorientation', handleOrientation);
        }
    }
});