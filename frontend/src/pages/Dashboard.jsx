import { useState, useEffect } from 'react';
import { getTeam, updateMyStatus, STATUS_OPTIONS } from '../api';
import { useAuth } from '../context/AuthContext';

// Status badge colors
const STATUS_COLORS = {
  'Working': '#10b981',
  'Working Remotely': '#3b82f6',
  'On Vacation': '#f59e0b',
  'Business Trip': '#8b5cf6',
};

function formatTimestamp(timestamp) {
  const date = new Date(timestamp);
  const now = new Date();
  const diffMs = now - date;
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  
  return date.toLocaleDateString();
}

export default function Dashboard() {
  const [team, setTeam] = useState([]);
  const [filteredTeam, setFilteredTeam] = useState([]);
  const [selectedFilters, setSelectedFilters] = useState([]);
  const [myStatus, setMyStatus] = useState(null);
  const [isUpdating, setIsUpdating] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const { logout } = useAuth();

  // Fetch team on mount
  useEffect(() => {
    fetchTeam();
  }, []);

  // Apply filters when team or filters change
  useEffect(() => {
    if (selectedFilters.length === 0) {
      setFilteredTeam(team);
    } else {
      const filterLabels = selectedFilters.map(
        f => STATUS_OPTIONS.find(o => o.value === f)?.label
      );
      setFilteredTeam(team.filter(m => filterLabels.includes(m.status)));
    }
  }, [team, selectedFilters]);

  const fetchTeam = async () => {
    try {
      setIsLoading(true);
      const data = await getTeam();
      setTeam(data);
      setError('');
    } catch (err) {
      setError('Failed to load team data');
    } finally {
      setIsLoading(false);
    }
  };

  const handleStatusChange = async (newStatus) => {
    setIsUpdating(true);
    try {
      await updateMyStatus(newStatus);
      setMyStatus(newStatus);
      await fetchTeam(); // Refresh team list
    } catch (err) {
      setError('Failed to update status');
    } finally {
      setIsUpdating(false);
    }
  };

  const toggleFilter = (statusValue) => {
    setSelectedFilters(prev => {
      if (prev.includes(statusValue)) {
        return prev.filter(f => f !== statusValue);
      }
      return [...prev, statusValue];
    });
  };

  const clearFilters = () => {
    setSelectedFilters([]);
  };

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="header-title">
            <img src="/small_logo.svg" alt="Momentum" className="logo-icon" />
            <h1>Team Presence</h1>
          </div>
          <button onClick={logout} className="logout-button">
            Sign Out
          </button>
        </div>
      </header>

      <main className="dashboard-main">
        {/* Status Update Section */}
        <section className="status-section">
          <h2>Update Your Status</h2>
          <div className="status-buttons">
            {STATUS_OPTIONS.map(option => (
              <button
                key={option.value}
                onClick={() => handleStatusChange(option.value)}
                disabled={isUpdating}
                className={`status-button ${myStatus === option.value ? 'active' : ''}`}
                style={{
                  '--status-color': STATUS_COLORS[option.label],
                }}
              >
                <span className="status-dot" style={{ backgroundColor: STATUS_COLORS[option.label] }} />
                {option.label}
              </button>
            ))}
          </div>
        </section>

        {/* Filter Section */}
        <section className="filter-section">
          <div className="filter-header">
            <h2>Team Members</h2>
            <div className="filter-controls">
              <span className="filter-label">Filter:</span>
              {STATUS_OPTIONS.map(option => (
                <button
                  key={option.value}
                  onClick={() => toggleFilter(option.value)}
                  className={`filter-chip ${selectedFilters.includes(option.value) ? 'active' : ''}`}
                  style={{
                    '--chip-color': STATUS_COLORS[option.label],
                  }}
                >
                  {option.label}
                </button>
              ))}
              {selectedFilters.length > 0 && (
                <button onClick={clearFilters} className="clear-filters">
                  Clear
                </button>
              )}
            </div>
          </div>
        </section>

        {/* Error Message */}
        {error && <div className="error-banner">{error}</div>}

        {/* Team List */}
        <section className="team-section">
          {isLoading ? (
            <div className="loading">Loading team...</div>
          ) : filteredTeam.length === 0 ? (
            <div className="empty-state">
              {selectedFilters.length > 0 
                ? 'No team members match the selected filters'
                : 'No team members found'}
            </div>
          ) : (
            <div className="team-grid">
              {filteredTeam.map(member => (
                <div key={member.id} className="team-card">
                  <div className="member-avatar">
                    {member.full_name.split(' ').map(n => n[0]).join('')}
                  </div>
                  <div className="member-info">
                    <h3 className="member-name">{member.full_name}</h3>
                    <div className="member-status">
                      <span 
                        className="status-badge"
                        style={{ backgroundColor: STATUS_COLORS[member.status] }}
                      >
                        {member.status}
                      </span>
                    </div>
                    <p className="member-updated">
                      Updated {formatTimestamp(member.updated_at)}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

