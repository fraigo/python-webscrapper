
class MainView extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        data: [],
        search: "Python",
        loading: false
      }
      this.handleChange = this.handleChange.bind(this)
      this.handleClick = this.handleClick.bind(this)
      this.lastChange = 0
    }
    handleChange(event){
        this.setState({search: event.target.value});
    }
    handleClick(event){
        var self = this
        window.clearTimeout(this.lastChange)
        this.setState({data: []});
        this.lastChange = window.setTimeout(() => {
            self.loadData()
        }, 300);
    }
    loadData(){
        this.setState({loading: true});
        fetch('./search?q='+ this.state.search)
        .then(response => response.json())
        .then(data => { 
            this.setState({ data }) 
            this.setState({loading: false}) 
            });
    }
    render() {
      const listItems = this.state.data.map((item) =>
        <li key={item.id} className="collection-item">
            <a target="_blank" href={ "https://ca.indeed.com/" + item.link} ><b>{item.text}</b></a>
            <br/>
            <b>{item.comp}</b> [{item.pub}]
            <br/>
            <small>
            {item.desc}
            </small>
        </li>
      );
      return (
        <main>
            <h1>Job Search</h1>
            <div className="row">
                <div className="col"><input type="text" value={this.state.search} onChange={this.handleChange} /></div>
                <div className="col"><a className="waves-effect waves-light btn" onClick={this.handleClick} >Go</a></div>
            </div>
            
            <ul className="collection">
            {listItems}
            </ul>
            { this.state.loading ? <img width="100%" src="static/web/loading.gif" /> : null }
        </main>  
      );
    }
    componentDidMount() {
        this.loadData()
    }
}