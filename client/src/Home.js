import React from "react";
import { Link } from "react-router-dom";
import LoyolaLogo from "./loyola_logo.jpg";
import "./Home.css";

const Home = () => {
    return(
        <div className="home">
            <div className="titleSection">
                <h1 className="title">Loyola Thermal Image <br /> Registry</h1>
                <img src={LoyolaLogo} className="logo" />
            </div>

            <div className="buttons">
                <Link to="/logform">
                    <button>Log Form</button>
                </Link>
                <Link to="/viewlogs">
                    <button>View Logs</button>
                </Link>
            </div>

            <div className="author">By Rolando Santos</div>
        </div>
    );
};

export default Home;