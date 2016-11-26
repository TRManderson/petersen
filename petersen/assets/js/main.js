class NewUser extends React.Component {
    constructor() {
        super();
        this.state = {
            name: "",
            username: "",
            password: "",
            passwordConfirm: ""
        };
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event) {
        event.preventDefault();

        if (!this.state.name.match(/^\w* \w$/)) {
            alert("Please enter a valid name (i.e. Tom Manderson)");
            return false;
        }

        if (!this.state.username.match(/^[a-zA-Z0-9]{3,25}$/)) {
            alert("Please enter a valid username (3-25 characters containing only alphanumeric characters)");
            return false;
        }

        if (this.state.password.length < 4) {
            alert("Please enter a longer password (minimum 4 characters)");
            return false;
        }

        if (this.state.passwordConfirm != this.state.password) {
            alert("Two passwords are not equal.");
            return false;
        }

        alert("woot woot motherfuckers!");
    }

    render() {
        return (
            <div id = "new-user">
            <form onSubmit = {this.handleSubmit}>
                <label>Name:
                <input type = "text" value = {this.state.name} onChange = {(event) => {
                    this.setState({name: event.target.value});
                }}/>
                </label>

                <label>Username:
                <input type = "text" value = {this.state.username} onChange = {(event) => {
                    this.setState({username: event.target.value});
                }}/>
                </label>

                <label>Password:
                <input type = "password" value = {this.state.password} onChange = {(event) => {
                    this.setState({password: event.target.value});
                }}/>
                </label>

                <label>Confirm Password:
                <input type = "password" value = {this.state.passwordConfirm} onChange = {(event) => {
                    this.setState({passwordConfirm: event.target.value});
                }}/>
                </label>

                <input type = "submit" value = "Create User"/>
            </form>
            </div>
        );
    }
}

class Demo extends React.Component {
    render() {
        $.ajax({
            url: "/user/new",
            data: JSON.stringify({
                name: "neil",
                password: "password1",
            }),
            contentType: "application/json",
            processData: false,
            method: "POST",
            success: function(data){console.log(data);}
        });
        return (
            <div>
                <h1>Hello World</h1>
                <p>What's up</p>
            </div>
        );
    }
}

ReactDOM.render(
    <NewUser />,
    document.getElementById('root')
);
