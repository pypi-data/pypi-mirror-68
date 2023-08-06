/* eslint-disable no-underscore-dangle */
import { bindActionCreators } from 'redux';
import {
  ExampleAction
} from '../state/{{ folder_name }}/{{ folder_name }}.actions';

class {{ component_name }} {
  constructor({ dispatch, getState }) {
    this.actions = {};

    if({{ component_name }}.instance) {
      throw new Error('{{ component_name }} is singleton');
    }

    this._initiate(dispatch, getState);

    {{ component_name }}.instance = this;

    return this;
  }

  _initiate(dispatch, getState) {
    this.actions = this._getActions(dispatch);
    this._getState = getState;
  }

  _getActions(dispatch) {
    return {
      open: bindActionCreators(ExampleAction, dispatch),
    };
  }
}

export default {{ component_name }};
