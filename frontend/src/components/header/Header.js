import React from 'react';
import './Header.scss';
import {Link} from "react-router-dom";

class Header extends React.Component {
    render() {
        return (
            <div>
                <div className="header">
                    <h1>{this.props.site_name}</h1>
                    <h4>{this.props.page_name}</h4>
                </div>
                <nav className="navbar navbar-expand-lg navbar-light bg-light">
                    <button className="navbar-toggler" type="button" data-toggle="collapse"
                            data-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false"
                            aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"/>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarTogglerDemo01">
                        <ul className="navbar-nav mr-auto mt-2 mt-lg-0">
                            <li className="nav-item">
                                <Link to="/" className="nav-link fa fa-home"> Home</Link>
                            </li>
                            <li className="nav-item">
                                <Link to="/about" className="nav-link fa fa-info"> About US</Link>
                            </li>

                            <li className="nav-item">
                                <Link to="/settings" className="nav-link fa fa-gears"> Settings</Link>
                            </li>
                        </ul>
                    </div>
                    <ul className="navbar-nav mr-auto mt-2 mt-lg-0">
                        <li className="nav-item">
                            <Link to="/account" className="nav-link fa fa-user"> Account</Link>
                        </li>
                    </ul>
                </nav>
            </div>
        );
    }
}

export default Header