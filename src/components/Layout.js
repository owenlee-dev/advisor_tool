import { React } from "react";
import "../styles/Layout.scss";
import { Navbar, Nav, Container } from "react-bootstrap";
import { Link, Outlet } from "react-router-dom";

const Layout = () => {
  return (
    <div>
      <Navbar
        className="header-container"
        collapseOnSelect
        bg="dark"
        variant="dark"
        fixed="top"
      >
        <Container>
          <Navbar.Brand className="title" href="/dashboard">
            Student Tracking System
          </Navbar.Brand>
          <Nav className="nav-buttons">
            <Nav.Item className="tab">
              <Link to="/dashboard" className="nav-link">
                Dashboard
              </Link>
            </Nav.Item>

            <Nav.Item className="tab">
              <Link to="/configuration" className="nav-link">
                Configuration
              </Link>
            </Nav.Item>
          </Nav>
        </Container>
      </Navbar>
      <Outlet />
    </div>
  );
};
export default Layout;
