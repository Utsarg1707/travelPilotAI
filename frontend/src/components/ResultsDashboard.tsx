import React, { useState, useEffect } from 'react';
import { Plane, Hotel, CloudSun, DollarSign, Calendar, Info, FileText } from 'lucide-react';
import { PlanResponse } from '../types/travel';

type TabType = 'itinerary' | 'flights' | 'hotels' | 'weather' | 'budget' | 'markdown';

interface ResultsDashboardProps {
  planResponse: PlanResponse;
}

export const ResultsDashboard: React.FC<ResultsDashboardProps> = ({ planResponse }) => {
  const decision = planResponse.supervisor_decision;
  const itinerary = planResponse.itinerary;
  const flights = planResponse.flight_results;
  const hotels = planResponse.hotel_results;
  const weather = planResponse.weather_forecast;
  const budget = planResponse.budget_analysis;
  const selectedAgents = planResponse.selected_agents || [];

  const hasItinerary = selectedAgents.length > 0 
    ? selectedAgents.includes('itinerary') 
    : !!itinerary?.days?.length;

  const hasFlights = selectedAgents.length > 0
    ? selectedAgents.includes('flight')
    : !!flights?.options?.length;

  const hasHotels = selectedAgents.length > 0
    ? selectedAgents.includes('hotel')
    : !!hotels?.options?.length;

  const hasWeather = selectedAgents.length > 0
    ? selectedAgents.includes('weather')
    : !!weather;

  const hasBudget = selectedAgents.length > 0
    ? selectedAgents.includes('budget')
    : !!budget;

  const availableTabs: TabType[] = [
    hasItinerary ? ('itinerary' as const) : null,
    hasFlights ? ('flights' as const) : null,
    hasHotels ? ('hotels' as const) : null,
    hasWeather ? ('weather' as const) : null,
    hasBudget ? ('budget' as const) : null,
    'markdown' as const,
  ].filter(Boolean) as TabType[];

  const [activeTab, setActiveTab] = useState<TabType>(availableTabs[0] || 'markdown');

  useEffect(() => {
    if (availableTabs.length > 0 && !availableTabs.includes(activeTab)) {
      setActiveTab(availableTabs[0]);
    }
  }, [planResponse, availableTabs.join(',')]);

  if (!planResponse.final_response) return null;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Overview & Metadata Card */}
      <div className="glass-card" style={{ padding: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: '0.5rem' }}>
          <div>
            <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: '#f8fafc' }}>
              ✈️ {decision?.destinations && decision.destinations.length > 1 ? 'Multi-City Trip Plan' : 'Trip Plan'}: {decision?.destination || 'Destination'}
            </h2>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              Origin: <strong>{decision?.origin || 'Bangalore'}</strong> | Travelers: <strong>{decision?.travelers || 1}</strong> | Duration: <strong>{decision?.duration_days || 5} Days</strong>
            </p>
          </div>
          <span className={`badge ${planResponse.approval_status === 'approved' ? 'badge-success' : 'badge-warning'}`}>
            Status: {planResponse.approval_status}
          </span>
        </div>

        {decision?.routing_reason && (
          <div style={{ background: 'rgba(99, 102, 241, 0.1)', padding: '0.75rem 1rem', borderRadius: '8px', fontSize: '0.85rem', display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
            <Info size={16} color="#818cf8" />
            <span><strong>Supervisor Routing Metadata:</strong> {decision.routing_reason}</span>
          </div>
        )}

        {/* Dashboard Navigation Tabs */}
        <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1.25rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.5rem', overflowX: 'auto' }}>
          {hasItinerary && (
            <button
              onClick={() => setActiveTab('itinerary')}
              className={`btn ${activeTab === 'itinerary' ? 'btn-primary' : 'btn-secondary'}`}
              style={{ padding: '0.4rem 0.9rem', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}
            >
              <Calendar size={15} /> Day-by-Day Itinerary
            </button>
          )}
          {hasFlights && (
            <button
              onClick={() => setActiveTab('flights')}
              className={`btn ${activeTab === 'flights' ? 'btn-primary' : 'btn-secondary'}`}
              style={{ padding: '0.4rem 0.9rem', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}
            >
              <Plane size={15} /> Flight Options ({flights?.options?.length || 0})
            </button>
          )}
          {hasHotels && (
            <button
              onClick={() => setActiveTab('hotels')}
              className={`btn ${activeTab === 'hotels' ? 'btn-primary' : 'btn-secondary'}`}
              style={{ padding: '0.4rem 0.9rem', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}
            >
              <Hotel size={15} /> Lodging Options ({hotels?.options?.length || 0})
            </button>
          )}
          {hasWeather && (
            <button
              onClick={() => setActiveTab('weather')}
              className={`btn ${activeTab === 'weather' ? 'btn-primary' : 'btn-secondary'}`}
              style={{ padding: '0.4rem 0.9rem', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}
            >
              <CloudSun size={15} /> Live Weather
            </button>
          )}
          {hasBudget && (
            <button
              onClick={() => setActiveTab('budget')}
              className={`btn ${activeTab === 'budget' ? 'btn-primary' : 'btn-secondary'}`}
              style={{ padding: '0.4rem 0.9rem', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}
            >
              <DollarSign size={15} /> Budget Analysis
            </button>
          )}
          <button
            onClick={() => setActiveTab('markdown')}
            className={`btn ${activeTab === 'markdown' ? 'btn-primary' : 'btn-secondary'}`}
            style={{ padding: '0.4rem 0.9rem', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}
          >
            <FileText size={15} /> Full Text Plan
          </button>
        </div>
      </div>

      {/* TAB 1: Day-by-Day Itinerary */}
      {activeTab === 'itinerary' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {itinerary && itinerary.days && itinerary.days.length > 0 ? (
            itinerary.days.map((day) => (
              <div key={day.day_number} className="glass-card" style={{ padding: '1.25rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem', flexWrap: 'wrap', gap: '0.5rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                    <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#38bdf8' }}>
                      🗓️ Day {day.day_number}: {day.theme}
                    </h3>
                    {day.destination_city && (
                      <span style={{ fontSize: '0.75rem', color: '#38bdf8', background: 'rgba(56,189,248,0.15)', padding: '0.15rem 0.5rem', borderRadius: '4px', fontWeight: 600 }}>
                        📍 {day.destination_city}
                      </span>
                    )}
                  </div>
                  <span style={{ fontSize: '0.8rem', color: '#a78bfa', background: 'rgba(167,139,250,0.1)', padding: '0.2rem 0.6rem', borderRadius: '4px' }}>
                    Est. Daily Cost: ₹{day.daily_cost_inr.toLocaleString('en-IN')}
                  </span>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                  {day.activities.map((act, idx) => (
                    <div key={idx} style={{ background: 'rgba(0,0,0,0.25)', borderLeft: '3px solid #6366f1', padding: '0.75rem 1rem', borderRadius: '0 8px 8px 0' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '0.25rem' }}>
                        <span style={{ fontWeight: 600, color: '#f8fafc' }}>{act.activity_title}</span>
                        <span style={{ color: '#94a3b8', fontSize: '0.75rem' }}><code>{act.time_slot}</code></span>
                      </div>
                      <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', margin: '0.25rem 0' }}>{act.description}</p>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#64748b', marginTop: '0.4rem' }}>
                        <span>📍 Location: <strong>{act.location}</strong></span>
                        <span>Est. Cost: <strong>₹{act.cost_inr.toLocaleString('en-IN')}</strong></span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))
          ) : (
            <div className="glass-card" style={{ padding: '2rem', textAlign: 'center' }}>
              <p style={{ color: 'var(--text-muted)' }}>Detailed day-by-day itinerary is rendered in the Full Text Plan tab.</p>
            </div>
          )}
        </div>
      )}

      {/* TAB 2: Flight Options */}
      {activeTab === 'flights' && (
        <div className="glass-card" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '1rem', color: '#38bdf8' }}>
            ✈️ Flight Search Results (MCP Live Search)
          </h3>
          {flights && flights.options && flights.options.length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {flights.options.map((f, idx) => (
                <div key={idx} style={{ background: 'rgba(0,0,0,0.3)', padding: '1rem', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
                  <div>
                    <h4 style={{ fontSize: '1rem', fontWeight: 700, color: '#f8fafc' }}>{f.airline} <span style={{ fontSize: '0.8rem', color: '#a78bfa' }}>({f.flight_number})</span></h4>
                    <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', margin: '0.25rem 0' }}>
                      Departure: <strong>{f.departure_time}</strong> → Arrival: <strong>{f.arrival_time}</strong> ({f.duration})
                    </p>
                    <span style={{ fontSize: '0.75rem', color: '#64748b' }}>Stops: {f.stops === 0 ? 'Non-stop Direct' : `${f.stops} Stop`}</span>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#34d399' }}>₹{f.total_price_inr.toLocaleString('en-IN')}</div>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>₹{f.price_inr.toLocaleString('en-IN')} / passenger</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p style={{ color: 'var(--text-muted)' }}>No flight search results available.</p>
          )}
        </div>
      )}

      {/* TAB 3: Lodging Options */}
      {activeTab === 'hotels' && (
        <div className="glass-card" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '1rem', color: '#38bdf8' }}>
            🏨 Accommodation & Hotel Options (MCP Live Search)
          </h3>
          {hotels && hotels.options && hotels.options.length > 0 ? (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
              {hotels.options.map((h, idx) => (
                <div key={idx} style={{ background: 'rgba(0,0,0,0.3)', padding: '1.25rem', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <h4 style={{ fontSize: '1rem', fontWeight: 700, color: '#f8fafc' }}>{h.hotel_name}</h4>
                      <span style={{ background: 'rgba(251,191,36,0.15)', color: '#fbbf24', padding: '0.2rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 700 }}>
                        ⭐ {h.rating} / 5
                      </span>
                    </div>
                    <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', margin: '0.4rem 0' }}>📍 {h.location}</p>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.3rem', margin: '0.5rem 0' }}>
                      {h.amenities.map((am, aIdx) => (
                        <span key={aIdx} style={{ fontSize: '0.7rem', background: 'rgba(255,255,255,0.05)', color: '#94a3b8', padding: '0.15rem 0.4rem', borderRadius: '4px' }}>
                          {am}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div style={{ borderTop: '1px solid rgba(255,255,255,0.05)', paddingTop: '0.75rem', marginTop: '0.75rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>₹{h.price_per_night_inr.toLocaleString('en-IN')} / night</span>
                    <span style={{ fontSize: '1.1rem', fontWeight: 800, color: '#34d399' }}>₹{h.total_price_inr.toLocaleString('en-IN')}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p style={{ color: 'var(--text-muted)' }}>No lodging options available.</p>
          )}
        </div>
      )}

      {/* TAB 4: Live Weather */}
      {activeTab === 'weather' && (
        <div className="glass-card" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '0.5rem', color: '#38bdf8' }}>
            🌤️ Destination Weather Forecast (Open-Meteo Integration)
          </h3>
          {weather ? (
            <div>
              <p style={{ fontSize: '0.9rem', color: '#f8fafc', marginBottom: '1rem' }}>{weather.weather_summary}</p>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '0.75rem', marginBottom: '1rem' }}>
                {weather.forecast.map((w, idx) => (
                  <div key={idx} style={{ background: 'rgba(0,0,0,0.3)', padding: '0.75rem', borderRadius: '8px', textAlign: 'center' }}>
                    <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#a78bfa' }}>{w.date}</div>
                    <div style={{ fontSize: '1.2rem', margin: '0.3rem 0' }}>🌤️</div>
                    <div style={{ fontSize: '0.85rem', fontWeight: 700, color: '#f8fafc' }}>{w.temp_max_c}°C / {w.temp_min_c}°C</div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>{w.weather_condition}</div>
                  </div>
                ))}
              </div>
              {weather.recommendations && weather.recommendations.length > 0 && (
                <div style={{ background: 'rgba(255,255,255,0.03)', padding: '0.75rem 1rem', borderRadius: '6px' }}>
                  <h5 style={{ fontSize: '0.8rem', fontWeight: 700, color: '#fbbf24', marginBottom: '0.3rem' }}>Weather Tips:</h5>
                  <ul style={{ fontSize: '0.8rem', color: 'var(--text-muted)', paddingLeft: '1.2rem', margin: 0 }}>
                    {weather.recommendations.map((r, rIdx) => (
                      <li key={rIdx}>{r}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <p style={{ color: 'var(--text-muted)' }}>No weather data available.</p>
          )}
        </div>
      )}

      {/* TAB 5: Budget Analysis */}
      {activeTab === 'budget' && (
        <div className="glass-card" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '1rem', color: '#38bdf8' }}>
            💰 Financial & Budget Analysis
          </h3>
          {budget ? (
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <div>
                  <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Estimated Total:</span>
                  <div style={{ fontSize: '1.5rem', fontWeight: 800, color: budget.within_budget ? '#34d399' : '#f87171' }}>
                    ₹{budget.estimated_total.toLocaleString('en-IN')}
                  </div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Budget Limit:</span>
                  <div style={{ fontSize: '1.2rem', fontWeight: 700, color: '#f8fafc' }}>
                    ₹{budget.budget_limit.toLocaleString('en-IN')}
                  </div>
                </div>
              </div>

              {/* Progress Bar */}
              <div style={{ background: 'rgba(255,255,255,0.1)', height: '10px', borderRadius: '5px', overflow: 'hidden', marginBottom: '1.5rem' }}>
                <div
                  style={{
                    background: budget.within_budget ? 'linear-gradient(90deg, #34d399, #059669)' : 'linear-gradient(90deg, #f87171, #dc2626)',
                    width: `${Math.min(100, (budget.estimated_total / (budget.budget_limit || 1)) * 100)}%`,
                    height: '100%',
                  }}
                />
              </div>

              <h4 style={{ fontSize: '0.9rem', fontWeight: 700, marginBottom: '0.75rem', color: '#f8fafc' }}>Categorized Expenses</h4>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '0.75rem' }}>
                <div style={{ background: 'rgba(0,0,0,0.25)', padding: '0.75rem', borderRadius: '6px' }}>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>✈️ Flights</span>
                  <div style={{ fontSize: '1rem', fontWeight: 700 }}>₹{budget.cost_breakdown.flights.toLocaleString('en-IN')}</div>
                </div>
                <div style={{ background: 'rgba(0,0,0,0.25)', padding: '0.75rem', borderRadius: '6px' }}>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>🏨 Accommodation</span>
                  <div style={{ fontSize: '1rem', fontWeight: 700 }}>₹{budget.cost_breakdown.accommodation.toLocaleString('en-IN')}</div>
                </div>
                <div style={{ background: 'rgba(0,0,0,0.25)', padding: '0.75rem', borderRadius: '6px' }}>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>🍽️ Food & Dining</span>
                  <div style={{ fontSize: '1rem', fontWeight: 700 }}>₹{budget.cost_breakdown.food.toLocaleString('en-IN')}</div>
                </div>
                <div style={{ background: 'rgba(0,0,0,0.25)', padding: '0.75rem', borderRadius: '6px' }}>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>🚕 Local Transport</span>
                  <div style={{ fontSize: '1rem', fontWeight: 700 }}>₹{budget.cost_breakdown.transport.toLocaleString('en-IN')}</div>
                </div>
                <div style={{ background: 'rgba(0,0,0,0.25)', padding: '0.75rem', borderRadius: '6px' }}>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>🎟️ Tours & Activities</span>
                  <div style={{ fontSize: '1rem', fontWeight: 700 }}>₹{budget.cost_breakdown.activities.toLocaleString('en-IN')}</div>
                </div>
                <div style={{ background: 'rgba(0,0,0,0.25)', padding: '0.75rem', borderRadius: '6px' }}>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>🛍️ Misc Buffer</span>
                  <div style={{ fontSize: '1rem', fontWeight: 700 }}>₹{budget.cost_breakdown.miscellaneous.toLocaleString('en-IN')}</div>
                </div>
              </div>
            </div>
          ) : (
            <p style={{ color: 'var(--text-muted)' }}>No budget analysis available.</p>
          )}
        </div>
      )}

      {/* TAB 6: Full Markdown Text */}
      {activeTab === 'markdown' && (
        <div className="glass-card" style={{ padding: '2rem' }}>
          <div style={{ whiteSpace: 'pre-line', fontSize: '0.95rem', lineHeight: 1.7, color: '#f8fafc' }}>
            {planResponse.final_response}
          </div>
        </div>
      )}

      {/* Tool Call Audit Log */}
      {planResponse.tool_calls && planResponse.tool_calls.length > 0 && (
        <div className="glass-card" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '1rem', color: 'var(--text-muted)' }}>
            🛠️ Model Context Protocol (MCP) Executed Tools Audit Log
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {planResponse.tool_calls.map((t, idx) => (
              <div key={idx} style={{ background: 'rgba(0, 0, 0, 0.3)', padding: '0.6rem 1rem', borderRadius: '8px', fontSize: '0.8rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <span style={{ fontWeight: 600, color: '#38bdf8' }}>[{t.agent_name}]</span> call <code style={{ color: '#a78bfa' }}>{t.tool_name}</code>
                  <span style={{ color: 'var(--text-muted)', marginLeft: '0.5rem' }}>— {t.result_summary}</span>
                </div>
                <span style={{ fontSize: '0.7rem', color: '#94a3b8' }}>{t.execution_time_ms} ms</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
