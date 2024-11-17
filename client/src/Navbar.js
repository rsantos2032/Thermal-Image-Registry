import { Link } from "react-router-dom";
import "./Navbar.css";
import LoyolaLogo from "./loyola_logo.jpg";

const Navbar = () => {
    return (
        <nav className="navbar">
            <h1>Loyola Thermal Image Registry</h1>
            <img src={LoyolaLogo} className="logo" />
           <div className="links">
                <Link to="/logform">Log Form</Link>
                <Link to="/viewlogs">View Logs</Link>
            </div>
        </nav>
    );
};


export default Navbar;