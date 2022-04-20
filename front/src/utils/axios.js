import axios from 'axios';
import utils from "./utils"

export default axios.create(utils.methods.getHeader());
