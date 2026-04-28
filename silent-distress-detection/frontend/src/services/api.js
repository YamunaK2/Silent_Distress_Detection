const API_URL = "https://silent-distress-detection.onrender.com";

export const getSystemStatus = async () => {
    try {
        const response = await fetch(`${API_URL}/status`);
        if (!response.ok) throw new Error("Network response was not ok");
        return await response.json();
    } catch (error) {
        console.error("Error fetching status:", error);
        return null;
    }
};

export const startMonitoring = async () => {
    try {
        const response = await fetch(`${API_URL}/start`, { method: 'POST' });
        return await response.json();
    } catch (error) {
        console.error("Error starting monitoring:", error);
    }
}

export const stopMonitoring = async () => {
    try {
        const response = await fetch(`${API_URL}/stop`, { method: 'POST' });
        return await response.json();
    } catch (error) {
        console.error("Error stopping monitoring:", error);
    }
}
