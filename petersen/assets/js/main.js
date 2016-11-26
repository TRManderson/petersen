class Demo extends React.Component {
    render() {
        $.ajax({
            url: "/user/new",
            data: JSON.stringify({
                name: "neil"
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
    <Demo />,
    document.getElementById('root')
);
