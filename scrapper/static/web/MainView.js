
class MainView extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        data: [],
        search: "Python",
        loading: false
      }
      this.handleChange = this.handleChange.bind(this)
      this.handleSubmit = this.handleSubmit.bind(this)
      this.lastChange = 0
    }
    handleChange(event){
        this.setState({search: event.target.value});
    }
    handleSubmit(event){
        event.preventDefault();
        var self = this
        window.clearTimeout(this.lastChange)
        this.setState({data: []});
        this.lastChange = window.setTimeout(() => {
            self.loadData()
        }, 300);
        return false;
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
        <main >
            <div className="container">
            <div className="row sticky">
                    <div className="col s12 m7 left">
                        <h3 >Job Search</h3>
                    </div>
                    <div className="col s12 m5">
                        <div className="col s12" id="searchContainer">
                            <form onSubmit={this.handleSubmit}>
                                <input id="searchTerm" type="text" placeholder="Search term" value={this.state.search} onChange={this.handleChange} />
                                <span id="searchButton" className="waves-effect waves-light btn right" onClick={this.handleSubmit} >Go</span>
                            </form>
                        </div>
                    </div>
                
            </div>
            
            
            <ul className="collection">
            {listItems}
            </ul>
            { this.state.loading ? <img width="100%" src="static/web/loading.gif" /> : null }
            </div>
        </main>  
      );
    }
    componentDidMount() {
        this.loadData()
    }
}