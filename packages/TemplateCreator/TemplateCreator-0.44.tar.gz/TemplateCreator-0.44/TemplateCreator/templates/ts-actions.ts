import createAsyncAction from '../../../utils/createAsyncAction';
import EndPoints from '../../../swagger2Ts/endpoints';
import { HttpService } from 'grid-services-ui-commons';


export enum {{ component_name }}ActionTypes {
  EXAMPLE = '@@{{ folder_name }}/EXAMPLE'
}

export const ExampleAction: () => Promise<
  void
> = createAsyncAction({{ component_name }}ActionTypes.EXAMPLE, (text: string) => {
  const options = EndPoints.example;
  return HttpService.fetch({ ...options, body: text });
});

export interface {{ component_name }}Action {
  type: {{ component_name }}ActionTypes.EXAMPLE;
}
