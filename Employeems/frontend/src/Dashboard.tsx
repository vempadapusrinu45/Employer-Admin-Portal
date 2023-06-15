import React, { useEffect } from 'react';
import 'bootstrap-icons/font/bootstrap-icons.css';
import { Link, Outlet, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './style.css'; // Import the CSS file

function Dashboard() {
  const navigate = useNavigate();
  axios.defaults.withCredentials = true;
  
  useEffect(() => {
    axios.get('http://localhost:8081/dashboard')
      .then(res => {
        if (res.data.Status === 'Success') {
          if (res.data.role === 'admin') {
            navigate('/');
          } else {
            const id = res.data.id;
            navigate('/employeedetail/' + id);
          }
        } else {
          navigate('/start');
        }
      })
      .catch(err => console.log(err));
  }, []);

  const handleLogout = () => {
    axios.get('http://localhost:8081/logout')
      .then(res => {
        navigate('/start');
      })
      .catch(err => console.log(err));
  };

  return (
    <div className="dashboard-container">
      <div className="sidebar">
        <Link to="/" className="logo">
          <span className="fs-5 fw-bolder">Admin Dashboard</span>
        </Link>
        <ul className="menu">
          <li>
            <Link to="/" className="menu-link">
              <i className="bi bi-speedometer2"></i> <span>Dashboard</span>
            </Link>
          </li>
          <li>
            <Link to="/employee" className="menu-link">
              <i className="bi bi-people"></i> <span>Manage Employees</span>
            </Link>
          </li>
          <li>
            <Link to="profile" className="menu-link">
              <i className="bi bi-person"></i> <span>Profile</span>
            </Link>
          </li>
          <li onClick={handleLogout}>
            <a href="#" className="menu-link">
              <i className="bi bi-power"></i> <span>Logout</span>
            </a>
          </li>
        </ul>
      </div>
      <div className="content">
        <div className="header">
          <h4 >Employee Management System</h4>
        </div>
          <Outlet />
      </div>
    </div>
  );
}

export default Dashboard;
