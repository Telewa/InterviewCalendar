import React from 'react';
import ReactDOM from 'react-dom';
import './index.scss';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import '../node_modules/jquery/dist/jquery.min.js';
import '../node_modules/popper.js';
import '../node_modules/bootstrap/dist/js/bootstrap.min.js';
import * as serviceWorker from './serviceWorker';
import AppRoutes from "./routes";

ReactDOM.render(<AppRoutes />, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
