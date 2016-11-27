let {Button, ControlLabel, FormControl, FormGroup, Nav, NavItem, PageHeader,
    Panel} = ReactBootstrap;

class LogIn extends React.Component {
    /* login window */
    constructor() {
        /* initialises the window itself, and data within it */
        super();
        this.state = {
            username: "",
            password: "",
        };
    }

    handle(event) {
        event.preventDefault();
        $.ajax({
            url: "/login",
            data: JSON.stringify({
                username: this.state.username,
                password: this.state.password
            }),
            contentType: "application/json",
            processData: false,
            method: "POST",
            success: (data) => this.props.login(data)
        });
    }

    render() {
        /* draw all of the things */
        return (
            <Panel>
            <PageHeader>Log In</PageHeader>
            <form onSubmit = {this.handle.bind(this)}>

            <FormGroup
                controlId = "username"
                validationState = "success"
            >
                <ControlLabel>User Name</ControlLabel>
                <FormControl
                    type = "text"
                    value = {this.state.name}
                    placeholder = "Your User Name Here"
                    onChange = {(event) => {
                        this.setState({username: event.target.value});
                    }}
                />
            </FormGroup>

            <FormGroup
                controlId = "password"
                validationState = "success"
            >
                <ControlLabel>Password</ControlLabel>
                <FormControl
                    type = "password"
                    value = {this.state.password}
                    onChange = {(event) => {
                        this.setState({password: event.target.value});
                    }}
                />
            </FormGroup>

            <Button
                type = "submit"
            >
                Log In
            </Button>
            </form>
            </Panel>
        );
    }
}

class NewUser extends React.Component {
    /* new user dialog window */
    constructor() {
        /* initialises the window itself, and data within it */
        super();
        this.state = {
            name: "",
            username: "",
            password: "",
            passwordConfirm: "",
        };
    }

    validateName() {
        /* ensures that the "name" field contains two words */
        if (!this.state.name.match(/^\w+ \w+$/)) {
            return "error";
        }
        return "success";
    }
    validateUserName() {
        /* ensures that the username field is between 3 and 25 characters long,
         * containing only alphanumeric characters */
        if (!this.state.username.match(/^\w{3,25}$/)) {
            return "error";
        }
        return "success";
    }
    validatePassword() {
        /* ensures that the password entered is more than 6 characters long */
        if (this.state.password.length <= 6) {
            return "error";
        }
        return "success";
    }
    validatePasswordConfirm() {
        /* ensures that the password confirm field matches the main password
         * field */
        if (this.state.passwordConfirm != this.state.password ||
                this.state.passwordConfirm.length <= 6) {
            return "error";
        }
        return "success";
    }

    handle(event) {
        /* determines if inputs are valid or not, and calls relevant handler */
        event.preventDefault();
        if (this.validateName() == "success" &&
                this.validateUserName() == "success" &&
                this.validatePassword() == "success" &&
                this.validatePasswordConfirm() == "success") {
            this.handleValid();
        }
    }
    handleValid() {
        /* makes the relevant API call, and calls parent's login function:
         * @todo */
        $.ajax({
            url: "/user/new",
            data: JSON.stringify({
                name: this.state.name,
                username: this.state.username,
                password: this.state.password
            }),
            contentType: "application/json",
            processData: false,
            method: "POST",
            success: (data) => this.props.login(data)
        });
    }

    render() {
        /* draw all of the things */
        return (
            <Panel>
            <PageHeader>Create New User</PageHeader>
            <form onSubmit = {this.handle.bind(this)}>

            <FormGroup
                controlId = "name"
                validationState = {this.validateName()}
            >
                <ControlLabel>Name</ControlLabel>
                <FormControl
                    type = "text"
                    value = {this.state.name}
                    placeholder = "Your Name Here"
                    onChange = {(event) => {
                        this.setState({name: event.target.value});
                    }}
                />
            </FormGroup>

            <FormGroup
                controlId = "username"
                validationState = {this.validateUserName()}
            >
                <ControlLabel>User Name</ControlLabel>
                <FormControl
                    type = "text"
                    value = {this.state.username}
                    placeholder = "Your User Name Here"
                    onChange = {(event) => {
                        this.setState({username: event.target.value});
                    }}
                />
            </FormGroup>

            <FormGroup
                controlId = "password"
                validationState = {this.validatePassword()}
            >
                <ControlLabel>Password</ControlLabel>
                <FormControl
                    type = "password"
                    value = {this.state.password}
                    onChange = {(event) => {
                        this.setState({password: event.target.value});
                    }}
                />
            </FormGroup>

            <FormGroup
                controlId = "passwordConfirm"
                validationState = {this.validatePasswordConfirm()}
            >
                <ControlLabel>Confirm Password</ControlLabel>
                <FormControl
                    type = "password"
                    value = {this.state.passwordConfirm}
                    onChange = {(event) => {
                        this.setState({passwordConfirm: event.target.value});
                    }}
                />
            </FormGroup>

            <Button
                type = "submit"
            >
                Create New User
            </Button>
            </form>
            </Panel>
        );
    }
}

class Welcome extends React.Component {
    /* offers the user either a "New User" dialog, or a "Log In" dialog */
    constructor() {
        /* initialises the window itself, and the data within it */
        super();
        this.state = {
            option: 1
        };
    }

    login(data) {
        console.log(data);
        if (data.error) {
            alert(data.error);
        } else {
            this.login(data);
        }
    }

    render() {
        /* draw all of the things */
        if (this.state.option == 1) {
            return (
                <Panel>
                <Nav
                    bsStyle = "pills"
                    activeKey = {1}
                    onSelect = {(select) => {
                        this.setState({option: select});
                    }}
                >
                    <NavItem eventKey = {1}>Log In</NavItem>
                    <NavItem eventKey = {2}>New User</NavItem>
                </Nav>

                <LogIn
                    login = {(data) => this.login(data)}
                />
                </Panel>
            );
        } else {
            return (
                <Panel>
                <Nav
                    bsStyle = "pills"
                    activeKey = {2}
                    onSelect = {(select) => {
                        this.setState({option: select});
                    }}
                >
                    <NavItem eventKey = {1}>Log In</NavItem>
                    <NavItem eventKey = {2}>New User</NavItem>
                </Nav>

                <NewUser
                    login = {(data) => this.login(data)}
                />
                </Panel>
            );
        }
    }
}

ReactDOM.render(
    <Welcome login = {(data) => {alert(data);}}/>,
    document.getElementById('root')
);
