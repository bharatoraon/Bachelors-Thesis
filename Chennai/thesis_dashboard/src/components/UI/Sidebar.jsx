import React from 'react';

// Toggle button definitions
const LAYER_TOGGLES = [
    {
        key: 'metro_blue',
        label: 'Metro Blue Line',
        emoji: '🔵',
        color: '#1E90FF',
        glow: 'rgba(30,144,255,0.5)',
    },
    {
        key: 'metro_green',
        label: 'Metro Green Line',
        emoji: '🟢',
        color: '#32DC8C',
        glow: 'rgba(50,220,140,0.5)',
    },
    {
        key: 'suburban',
        label: 'Suburban Rail',
        emoji: '🚆',
        color: '#FF8C1E',
        glow: 'rgba(255,140,30,0.5)',
    },
    {
        key: 'bus',
        label: 'MTC Bus Routes',
        emoji: '🚌',
        color: '#B464FF',
        glow: 'rgba(180,100,255,0.4)',
    },
    {
        key: 'stops',
        label: 'Station Nodes',
        emoji: '⬤',
        color: '#94A3B8',
        glow: null,
    },
    {
        key: 'hotspots',
        label: 'Friction Hotspots',
        emoji: '🔥',
        color: '#FF5050',
        glow: 'rgba(255,80,80,0.5)',
    },
];

const styles = {
    sidebar: {
        position: 'absolute',
        top: '16px',
        left: '16px',
        width: '300px',
        maxHeight: 'calc(100vh - 32px)',
        overflowY: 'auto',
        zIndex: 10,
        background: 'rgba(8, 14, 32, 0.84)',
        backdropFilter: 'blur(24px)',
        WebkitBackdropFilter: 'blur(24px)',
        border: '1px solid rgba(255,255,255,0.09)',
        borderRadius: '20px',
        padding: '22px',
        boxShadow: '0 24px 60px rgba(0,0,0,0.7), inset 0 1px 0 rgba(255,255,255,0.06)',
        display: 'flex',
        flexDirection: 'column',
        gap: '16px',
        scrollbarWidth: 'none',
    },
    heading: {
        fontSize: '19px',
        fontWeight: 800,
        background: 'linear-gradient(135deg, #60a5fa 0%, #34d399 100%)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        backgroundClip: 'text',
        lineHeight: 1.2,
    },
    subtitle: {
        fontSize: '10px',
        letterSpacing: '0.1em',
        textTransform: 'uppercase',
        fontWeight: 600,
        color: 'rgba(150,160,190,0.8)',
        marginTop: '3px',
    },
    sectionTitle: {
        fontSize: '10px',
        fontWeight: 700,
        color: 'rgba(180,190,220,0.6)',
        textTransform: 'uppercase',
        letterSpacing: '0.1em',
        marginBottom: '8px',
    },
    divider: {
        height: '1px',
        background: 'rgba(255,255,255,0.07)',
    },
    metricsGrid: {
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '8px',
    },
    metricCard: {
        background: 'rgba(255,255,255,0.04)',
        border: '1px solid rgba(255,255,255,0.07)',
        borderRadius: '12px',
        padding: '12px',
    },
    metricLabel: {
        fontSize: '10px',
        color: 'rgba(150,160,180,0.8)',
        marginBottom: '4px',
    },
    metricBadge: {
        fontSize: '10px',
        color: 'rgba(130,145,175,0.7)',
        marginTop: '3px',
    },
    modeRow: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '9px 12px',
        background: 'rgba(255,255,255,0.03)',
        border: '1px solid rgba(255,255,255,0.06)',
        borderRadius: '10px',
        marginBottom: '6px',
    },
    modeLabel: {
        fontSize: '12px',
        color: 'rgba(200,210,230,0.85)',
    },
    // Toggle pill button
    toggleRow: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '10px 14px',
        borderRadius: '12px',
        marginBottom: '6px',
        border: '1px solid rgba(255,255,255,0.07)',
        background: 'rgba(255,255,255,0.03)',
        cursor: 'pointer',
        transition: 'background 0.2s',
        userSelect: 'none',
    },
};

function ToggleSwitch({ on, color, glow }) {
    // No onClick here — the parent toggleRow div handles it.
    // Adding e.stopPropagation on the pill itself prevents any accidental bubbling.
    return (
        <div
            style={{
                width: '38px',
                height: '20px',
                borderRadius: '10px',
                background: on ? color : 'rgba(255,255,255,0.12)',
                boxShadow: on && glow ? `0 0 8px ${glow}` : 'none',
                position: 'relative',
                transition: 'background 0.25s, box-shadow 0.25s',
                cursor: 'pointer',
                flexShrink: 0,
            }}
        >
            <div style={{
                position: 'absolute',
                top: '2px',
                left: on ? '18px' : '2px',
                width: '16px',
                height: '16px',
                borderRadius: '50%',
                background: 'white',
                transition: 'left 0.2s',
                boxShadow: '0 1px 4px rgba(0,0,0,0.4)',
            }} />
        </div>
    );
}

export default function Sidebar({ layerVisibility, toggleLayer }) {
    return (
        <div style={styles.sidebar}>

            {/* Header */}
            <div>
                <div style={styles.heading}>Chennai Transport Friction</div>
                <div style={styles.subtitle}>Spatial-Temporal Inequity Dashboard</div>
            </div>

            <div style={styles.divider} />

            {/* Metrics */}
            <div>
                <div style={styles.sectionTitle}>Network Insights</div>
                <div style={styles.metricsGrid}>
                    <div style={styles.metricCard}>
                        <div style={styles.metricLabel}>Gini Coefficient</div>
                        <div style={{ fontSize: '24px', fontWeight: 800, color: '#60a5fa' }}>0.277</div>
                        <div style={styles.metricBadge}>Moderate Inequality</div>
                    </div>
                    <div style={styles.metricCard}>
                        <div style={styles.metricLabel}>Avg Transfer Burden</div>
                        <div style={{ fontSize: '24px', fontWeight: 800, color: '#fbbf24' }}>26 <span style={{ fontSize: '13px', fontWeight: 400 }}>min</span></div>
                        <div style={styles.metricBadge}>Wait + Walk Penalty</div>
                    </div>
                    <div style={styles.metricCard}>
                        <div style={styles.metricLabel}>Policy Impact (Sync)</div>
                        <div style={{ fontSize: '24px', fontWeight: 800, color: '#34d399' }}>−24%</div>
                        <div style={styles.metricBadge}>Friction Reduction</div>
                    </div>
                    <div style={styles.metricCard}>
                        <div style={styles.metricLabel}>Total Stations</div>
                        <div style={{ fontSize: '24px', fontWeight: 800, color: 'rgba(220,230,250,0.9)' }}>8,107</div>
                        <div style={styles.metricBadge}>Mapped Nodes</div>
                    </div>
                </div>
            </div>

            <div style={styles.divider} />

            {/* Friction by Mode */}
            <div>
                <div style={styles.sectionTitle}>Avg Friction by Mode</div>
                <div style={styles.modeRow}>
                    <span style={styles.modeLabel}>🚌 Bus (MTC)</span>
                    <span style={{ fontSize: '13px', fontWeight: 700, color: '#34d399' }}>21.7 min</span>
                </div>
                <div style={styles.modeRow}>
                    <span style={styles.modeLabel}>🚇 Metro (CMRL)</span>
                    <span style={{ fontSize: '13px', fontWeight: 700, color: '#fbbf24' }}>29.7 min</span>
                </div>
                <div style={styles.modeRow}>
                    <span style={styles.modeLabel}>🚆 Suburban Rail</span>
                    <span style={{ fontSize: '13px', fontWeight: 700, color: '#f87171' }}>41.9 min</span>
                </div>
            </div>

            <div style={styles.divider} />

            {/* Layer Toggles */}
            <div>
                <div style={styles.sectionTitle}>Map Layers</div>
                {LAYER_TOGGLES.map(({ key, label, emoji, color, glow }) => (
                    <div
                        key={key}
                        style={{
                            ...styles.toggleRow,
                            background: layerVisibility[key] ? `${color}12` : 'rgba(255,255,255,0.02)',
                            borderColor: layerVisibility[key] ? `${color}40` : 'rgba(255,255,255,0.07)',
                        }}
                        onClick={() => toggleLayer(key)}
                    >
                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                            <span style={{ fontSize: '14px' }}>{emoji}</span>
                            <span style={{
                                fontSize: '12px',
                                fontWeight: 500,
                                color: layerVisibility[key] ? color : 'rgba(180,190,210,0.6)',
                                transition: 'color 0.2s',
                            }}>{label}</span>
                        </div>
                        <ToggleSwitch
                            on={layerVisibility[key]}
                            color={color}
                            glow={glow}
                        />
                    </div>
                ))}
            </div>

        </div>
    );
}
