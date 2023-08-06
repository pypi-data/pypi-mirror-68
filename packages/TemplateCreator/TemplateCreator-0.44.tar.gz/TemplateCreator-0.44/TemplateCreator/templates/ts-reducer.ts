import { AnyAction, Reducer } from 'redux';
import {{ folder_name }}InitialState, { {{ component_name }}State } from './{{ folder_name }}.state';
import { {{ component_name }}ActionTypes } from './{{ folder_name }}.actions';
import { SUCCESS_SUFFIX } from '../../constants';
import EndPoints from '../../../swagger2Ts/endpoints';


const {{ folder_name }}Reducer: Reducer<{{ component_name }}State> = (
    state: {{ component_name }}State = {{ folder_name }}InitialState,
    action: AnyAction
) => {
    if (!action.payload) {
        return state;
    }
    switch (action.type) {
        case {%raw%}`${{%endraw%}{{ component_name }}ActionTypes.EXAMPLE}${SUCCESS_SUFFIX}`:
            return { ...state, example: action.payload }

        default:
            return state;
    }
};

export default {{ folder_name }}Reducer;
