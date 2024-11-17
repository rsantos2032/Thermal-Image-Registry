import LogForm from './LogForm';
import Home from './Home';
import ViewLogs from './ViewLogs';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

function App() {
  return(
    <Router>
      <Routes>
        <Route path="/" element={<Home />}/>
        <Route path="/logform" element={<LogForm />}/>
        <Route path="/viewlogs" element={<ViewLogs />}/>
      </Routes>
    </Router>
  );
};

export default App;
