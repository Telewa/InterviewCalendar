import React from 'react';
import './Footer.scss'

class Footer extends React.Component {
    render() {
        return (
            <div className="footer">
                &copy; {this.props.site_name} {this.props.year}
            </div>
        );
    }
}

export default Footer