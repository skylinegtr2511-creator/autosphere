import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [vehicles, setVehicles] = useState([]);
  const [searchQuery, setSearchQuery] = useState(''); // New state for the search bar
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('/api/vehicles/')
      .then(response => {
        setVehicles(response.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching data: ", err);
        setError("Failed to connect to the AutoSphere backend.");
        setLoading(false);
      });
  }, []);

  // Filter the vehicles based on what the user types in the search bar
  const filteredVehicles = vehicles.filter(car => {
    const fullName = `${car.year} ${car.make} ${car.model}`.toLowerCase();
    return fullName.includes(searchQuery.toLowerCase()) || car.engine_type.toLowerCase().includes(searchQuery.toLowerCase());
  });

  if (loading) return <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>🔄 Tuning engines... Loading vehicle database...</div>;
  if (error) return <div style={{ padding: '20px', color: 'red', fontFamily: 'sans-serif' }}>❌ {error}</div>;

  return (
    <div style={{ padding: '40px', fontFamily: 'sans-serif', backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
      <header style={{ marginBottom: '40px', borderBottom: '2px solid #dee2e6', paddingBottom: '20px' }}>
        <h1 style={{ margin: 0, color: '#1a252f' }}>🌐 AutoSphere</h1>
        <p style={{ color: '#6c757d', margin: '5px 0 0 0' }}>The Intelligent Automotive Encyclopedia & Community Hub</p>
      </header>

      <main>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2 style={{ color: '#2c3e50', margin: 0 }}>🏎️ Living Vehicle Database</h2>

          {/* THE NEW SEARCH BAR */}
          <input
            type="text"
            placeholder="Search by make, model, or engine..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{
              padding: '10px 15px',
              borderRadius: '20px',
              border: '1px solid #ced4da',
              width: '300px',
              outline: 'none',
              fontSize: '14px'
            }}
          />
        </div>

        {filteredVehicles.length === 0 ? (
          <p style={{ color: '#6c757d' }}>No vehicles match your search criteria. Try a different term!</p>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' }}>
            {filteredVehicles.map(car => (
              <div key={car.id} style={{ backgroundColor: '#fff', borderRadius: '8px', padding: '20px', boxShadow: '0 4px 6px rgba(0,0,0,0.05)', border: '1px solid #e9ecef' }}>
                <span style={{ fontSize: '12px', fontWeight: 'bold', color: '#3498db', textTransform: 'uppercase' }}>{car.drivetrain}</span>
                <h3 style={{ margin: '5px 0 10px 0', color: '#2c3e50' }}>{car.year} {car.make} {car.model}</h3>

                <div style={{ fontSize: '14px', color: '#495057', lineHeight: '1.6' }}>
                  <div><strong>Engine:</strong> {car.engine_type}</div>
                  <div><strong>Power:</strong> {car.horsepower} hp</div>
                  <div><strong>Torque:</strong> {car.torque_lbft} lb-ft</div>
                </div>

                <div style={{ marginTop: '15px', paddingTop: '15px', borderTop: '1px solid #f1f3f5', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontWeight: 'bold', color: '#2ecc71', fontSize: '16px' }}>
                    ${car.msrp_usd.toLocaleString()}
                  </span>
                  <span style={{ fontSize: '12px', color: '#adb5bd' }}>Est. MSRP</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;