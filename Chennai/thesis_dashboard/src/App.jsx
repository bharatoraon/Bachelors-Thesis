import { useState } from 'react';
import DeckMap from './components/Map/DeckMap';
import Sidebar from './components/UI/Sidebar';
import Tooltip from './components/UI/Tooltip';

// Initial visibility state for all toggleable layers
const DEFAULT_VISIBILITY = {
    metro_blue: true,
    metro_green: true,
    suburban: true,
    bus: true,
    stops: true,
    hotspots: true,
};

function App() {
    const [tooltipInfo, setTooltipInfo] = useState(null);
    const [layerVisibility, setLayerVisibility] = useState(DEFAULT_VISIBILITY);

    function toggleLayer(key) {
        setLayerVisibility(prev => ({ ...prev, [key]: !prev[key] }));
    }

    return (
        <div style={{ position: 'fixed', inset: 0, width: '100vw', height: '100vh', background: '#0b0f19' }}>
            <DeckMap setTooltipInfo={setTooltipInfo} layerVisibility={layerVisibility} />
            <Sidebar layerVisibility={layerVisibility} toggleLayer={toggleLayer} />
            <Tooltip info={tooltipInfo} />
        </div>
    );
}

export default App;
