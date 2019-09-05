import React, {Component} from 'react'
import FormComponent from '../form/FormComponent';
import Axios from 'axios';
import SchemaListComponent from '../schema-list/SchemaListComponent';
import { getBaseUrl } from '../../global';


const formName = 'Source'

class SourceServer extends Component {
    
    constructor() {
        super();
        this.state = {
            response: {}
        }
        this.formValue = {};
        this.submited = false;
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.createSource = this.createSource.bind(this);
        this.httpClient = Axios.create();
        this.httpClient.defaults.timeout = 1000;

    }

    handleChange(event) {
        const { name, value } = event.target;
        this.formValue[name] = value;
    }

    handleSubmit(e) {
        this.createSource();
        this.submited = true;
    }

    createSource() {
        Axios.post(`${getBaseUrl()}api/schemas`, this.formValue)
            .then((response) => {
                this.setState({ response: response.data });
            });
    }

    

    render() {
        if (!this.submited) {
            return (
                <FormComponent
                    formName={formName}
                    handleChange={this.handleChange}
                    handleSubmit={this.handleSubmit}
                    data={this.state}
                />
            );
        }
        else {
            return (
                <div>
                    <SchemaListComponent formName={formName} schemaList={this.state.response}></SchemaListComponent>
                </div>
            );
        }
    }
}

export default SourceServer;