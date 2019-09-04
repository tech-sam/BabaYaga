import React, {Component} from "react"
import './Header.scss'

class HeaderComponent extends Component {
    // constructor() {}

    render() {
        return (
            <section className='container'>
            <nav className="navbar navbar-text">
                <div className="navbar-brand"></div>
                BabaYaga
            </nav>
            </section>
        )
    }
}

export default HeaderComponent