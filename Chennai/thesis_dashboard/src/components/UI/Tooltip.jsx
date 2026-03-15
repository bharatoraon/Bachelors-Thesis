import React from 'react';

export default function Tooltip({ info }) {
    if (!info) return null;

    const tfi = info.TFI_minutes ? Number(info.TFI_minutes).toFixed(1) : '—';
    const waitMin = info.avg_wait_sec ? Math.round(info.avg_wait_sec / 60) : '—';
    const walkM = info.avg_walk_dist_m ? Math.round(info.avg_walk_dist_m) : '—';
    const isCritical = info.TFI_minutes > 100;
    const isHigh = info.TFI_minutes > 50 && !isCritical;

    const accentColor = isCritical ? '#f87171' : isHigh ? '#fbbf24' : '#34d399';
    const severity = isCritical ? 'Critical Bottleneck' : isHigh ? 'High Wait Zone' : 'Standard Node';

    return (
        <div style={{
            position: 'fixed',
            left: info.x + 16,
            top: info.y + 16,
            width: '240px',
            background: 'rgba(8,14,32,0.92)',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            border: `1px solid rgba(255,255,255,0.1)`,
            borderRadius: '16px',
            padding: '16px',
            boxShadow: `0 16px 40px rgba(0,0,0,0.7), 0 0 0 1px ${accentColor}30`,
            zIndex: 50,
            pointerEvents: 'none',
            fontFamily: 'Inter, system-ui, sans-serif',
        }}>
            {/* Header */}
            <div style={{ borderBottom: '1px solid rgba(255,255,255,0.08)', paddingBottom: '10px', marginBottom: '12px' }}>
                <div style={{ fontSize: '14px', fontWeight: 700, color: 'white', marginBottom: '3px', lineHeight: 1.3 }}>
                    {info.stop_name || 'Unknown Station'}
                </div>
                <div style={{ fontSize: '10px', fontWeight: 600, color: accentColor, textTransform: 'uppercase', letterSpacing: '0.08em' }}>
                    {severity}
                </div>
            </div>

            {/* TFI Score */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '12px' }}>
                <span style={{ fontSize: '11px', color: 'rgba(180,190,210,0.7)' }}>Transfer Friction:</span>
                <span style={{ fontSize: '22px', fontWeight: 800, color: accentColor }}>{tfi} <span style={{ fontSize: '12px', fontWeight: 400, color: 'rgba(200,210,220,0.6)' }}>min</span></span>
            </div>

            {/* Details */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px' }}>
                    <span style={{ color: 'rgba(160,170,200,0.7)' }}>⏱ Avg Wait</span>
                    <span style={{ color: 'white', fontWeight: 500 }}>{waitMin} min</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px' }}>
                    <span style={{ color: 'rgba(160,170,200,0.7)' }}>🚶 Walk Distance</span>
                    <span style={{ color: 'white', fontWeight: 500 }}>{walkM} m</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', paddingTop: '8px', borderTop: '1px solid rgba(255,255,255,0.07)' }}>
                    <span style={{ color: 'rgba(160,170,200,0.6)' }}>Mode</span>
                    <span style={{ color: 'rgba(210,220,240,0.9)', fontWeight: 500, textTransform: 'uppercase', fontSize: '11px' }}>{info.mode || 'mixed'}</span>
                </div>
            </div>
        </div>
    );
}
