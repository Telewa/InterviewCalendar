import React from 'react';
import PropTypes from 'prop-types';

export default function Nav(props) {
    const logged_out_nav = (
        <ul className="navbar-nav mt-2 mt-lg-0">
            <li className="nav-item" >
                <button type="button" className="nav-link fa fa-lock" onClick={() => props.display_form('login')}> login </button>
            </li>
            <li className="nav-item">
                <button type="button" className="nav-link fa fa-user" onClick={() => props.display_form('signup')}> Signup </button>
            </li>
        </ul>
    );

    const logged_in_nav = (
        <ul className="navbar-nav mt-2 mt-lg-0">
            <li  className="nav-item" >
                <button type="button" className="nav-link fa fa-unlock" onClick={props.handle_logout}> Sign out ({props.logged_in_user})</button>
            </li>
        </ul>
    );
    return props.logged_in ? logged_in_nav : logged_out_nav;
}


Nav.propTypes = {
    logged_in: PropTypes.bool.isRequired,
    display_form: PropTypes.func.isRequired,
    handle_logout: PropTypes.func.isRequired
};