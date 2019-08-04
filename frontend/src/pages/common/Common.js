import React from 'react';
import './Common.scss';
import './../../../node_modules/font-awesome/css/font-awesome.min.css'
import Header from "../../components/header/Header";
import Footer from "../../components/footer/Footer";


export default class Common extends React.Component {

    constructor(props) {
        super(props);

        this.site_name = "Interview Calendar";
        this.year = new Date().getFullYear();
        this.page_name = "Common";
    }

    body() {
        return (
            <div>
                Welcome to our {this.page_name} page
            </div>
        );
    }

    render() {
        return (
            <div className="app container-fluid">
                <Header site_name={this.site_name} page_name={this.page_name}/>
                {/*<Body site_name={this.site_name}/>*/}
                <div className="body">
                    {this.body()}
                </div>
                <Footer site_name={this.site_name} year={this.year}/>
            </div>
        );
    }
}