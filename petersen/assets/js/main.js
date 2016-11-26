class Demo extends React.Component {
    render() {
        $.ajax({
            url: "/index.html",
            success: function(data){alert(data);}
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
