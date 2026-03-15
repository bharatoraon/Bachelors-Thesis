import { useState, useEffect, useMemo, useCallback } from 'react';
import DeckGL from '@deck.gl/react';
import { GeoJsonLayer } from '@deck.gl/layers';
import Map from 'react-map-gl/maplibre';
import 'maplibre-gl/dist/maplibre-gl.css';
import { fetchGeoJsonData } from '../../utils/dataLoader';

const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json';

const INITIAL_VIEW_STATE = {
    longitude: 80.237,
    latitude: 13.060,
    zoom: 10.5,
    pitch: 40,
    bearing: 0,
};

// Layer color definitions per mode
const ROUTE_COLORS = {
    metro_blue: [30, 144, 255, 230],  // Electric blue
    metro_green: [50, 220, 140, 230],  // Emerald green
    suburban: [255, 140, 30, 220],  // Amber orange
    bus: [180, 100, 255, 100],  // Purple, semi-transparent (dense network)
};

export default function DeckMap({ setTooltipInfo, layerVisibility }) {
    const [allStops, setAllStops] = useState(null);
    const [hotspots, setHotspots] = useState(null);
    const [routes, setRoutes] = useState({
        metro_blue: null,
        metro_green: null,
        suburban: null,
        bus: null,
    });

    useEffect(() => {
        async function loadData() {
            const [stopsGeo, hotspotsGeo, metroBlue, metroGreen, suburban, bus] = await Promise.all([
                fetchGeoJsonData('/data/unified_stops.geojson'),
                fetchGeoJsonData('/data/spatial_friction_hotspots.geojson'),
                fetchGeoJsonData('/data/metro_blue_corridor.geojson'),
                fetchGeoJsonData('/data/metro_green_corridor.geojson'),
                fetchGeoJsonData('/data/suburban_corridor.geojson'),
                fetchGeoJsonData('/data/bus_routes.geojson'),
            ]);
            setAllStops(stopsGeo);
            setHotspots(hotspotsGeo);
            setRoutes({ metro_blue: metroBlue, metro_green: metroGreen, suburban, bus });
        }
        loadData();
    }, []);

    const handleHover = useCallback((info) => {
        setTooltipInfo(info.object ? { ...info.object.properties, x: info.x, y: info.y } : null);
    }, [setTooltipInfo]);

    const layers = useMemo(() => {
        const arr = [];

        // ── Base stops (background dots) ──────────────────────────────────────────
        if (allStops && layerVisibility.stops) {
            arr.push(new GeoJsonLayer({
                id: 'all-stops',
                data: allStops,
                pointType: 'circle',
                getPointRadius: 25,
                pointRadiusUnits: 'meters',
                getFillColor: (d) => {
                    const mode = d.properties?.mode;
                    if (mode === 'metro') return [30, 144, 255, 160];
                    if (mode === 'suburban') return [255, 140, 30, 150];
                    return [150, 140, 170, 80];
                },
                pickable: false,
                stroked: false,
            }));
        }

        // ── Route Lines ────────────────────────────────────────────────────────────
        const routeDefs = [
            { key: 'metro_blue', data: routes.metro_blue, color: ROUTE_COLORS.metro_blue, width: 4 },
            { key: 'metro_green', data: routes.metro_green, color: ROUTE_COLORS.metro_green, width: 4 },
            { key: 'suburban', data: routes.suburban, color: ROUTE_COLORS.suburban, width: 3 },
            { key: 'bus', data: routes.bus, color: ROUTE_COLORS.bus, width: 1.5 },
        ];

        for (const { key, data, color, width } of routeDefs) {
            if (data && layerVisibility[key]) {
                arr.push(new GeoJsonLayer({
                    id: `route-${key}`,
                    data,
                    getLineColor: color,
                    lineWidthMinPixels: width,
                    lineWidthMaxPixels: key === 'bus' ? 2 : 6,
                    lineCapRounded: true,
                    lineJointRounded: true,
                    filled: false,
                    stroked: true,
                    pickable: false,
                }));
            }
        }

        // ── Hotspot friction circles ───────────────────────────────────────────────
        if (hotspots && layerVisibility.hotspots) {
            arr.push(new GeoJsonLayer({
                id: 'hotspots',
                data: hotspots,
                pointType: 'circle',
                getPointRadius: (d) => Math.max(150, (d.properties?.TFI_minutes || 20) * 25),
                pointRadiusUnits: 'meters',
                getFillColor: (d) => {
                    const tfi = d.properties?.TFI_minutes || 0;
                    if (tfi > 100) return [255, 50, 50, 210];
                    if (tfi > 50) return [255, 175, 30, 200];
                    return [80, 230, 140, 180];
                },
                getLineColor: [255, 255, 255, 50],
                lineWidthMinPixels: 1,
                stroked: true,
                pickable: true,
                onHover: handleHover,
            }));
        }

        return arr;
    }, [allStops, hotspots, routes, handleHover, layerVisibility]);

    return (
        <div style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}>
            <DeckGL
                initialViewState={INITIAL_VIEW_STATE}
                controller={true}
                layers={layers}
                style={{ width: '100%', height: '100%' }}
            >
                <Map mapStyle={MAP_STYLE} />
            </DeckGL>
        </div>
    );
}
