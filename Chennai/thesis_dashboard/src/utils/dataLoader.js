import Papa from 'papaparse';

/**
 * Utility to fetch and parse CSV data asynchronously using PapaParse
 * Assumes the file sits in the public directory (e.g., '/data/filename.csv')
 */
export const fetchCsvData = (url) => {
    return new Promise((resolve, reject) => {
        Papa.parse(url, {
            download: true,
            header: true,
            dynamicTyping: true, // Auto convert strings to numbers
            skipEmptyLines: true,
            complete: (results) => {
                resolve(results.data);
            },
            error: (error) => {
                console.error(`Error loading CSV from ${url}:`, error);
                reject(error);
            }
        });
    });
};

/**
 * Utility to fetch GeoJSON from the public public directory.
 */
export const fetchGeoJsonData = async (url) => {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error loading GeoJSON from ${url}:`, error);
        return null;
    }
};
