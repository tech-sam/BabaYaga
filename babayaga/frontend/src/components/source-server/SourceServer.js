import React, {Component} from 'react'
import FormComponent from '../form/FormComponent';
import SchemaComponent from '../schema/SchemaComponent';
import todosData from '../test-data/test';
// import Axios from 'axios';


const formName = 'Source'

class SourceServer extends Component {
    
    constructor() {
        super()
        this.state = {
            hostName: "",
            port:"",
            databaseName: "",
            userName: "",
            password: "",
            schemaName: ""
        }
        this.submited = false;
        this.handleChange = this.handleChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
        this.createSource = this.createSource.bind(this)
    }

    handleChange(event) {
        const {name, value} = event.target
        this.setState({
            [name]: value
        })
    }

    handleSubmit(e) {
        console.log('SOURCE-DATA', this.state)
        this.createSource()
        e.preventDefault();
    }

    createSource(){
        // const response = Axios.post('http://127.0.0.1:8000/', this.state, {
        //     headers: { 'Content-Type': 'multipart/form-data' },
        // })
        this.response = todosData;
        this.schemas = this.response.map(schema => {
            return <SchemaComponent key={schema.id} schema={schema} />
        })
        this.submited = true;
        console.log('res', this.response)
        this.forceUpdate()
    }

    

    render() {
        if(!this.submited){
            return (
                <FormComponent
                formName={formName}
                handleChange={this.handleChange}
                handleSubmit={this.handleSubmit}
                data={this.state}
                />    
            )
        }
        return (
            <div>
                {this.schemas}
            </div>
        )
    }
}

export default SourceServer