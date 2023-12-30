import { ActionNodeInput, AutomationActionType, AutomationHTTPContentType, AutomationHTTPMethod, AutomationParametersType, AutomationTriggerType, UpdateWorkflowMutationInput } from '@karrio/types/graphql/ee';
import { WorkflowTriggerType, WorkflowType, useWorkflow, useWorkflowMutation } from '@karrio/hooks/workflows';
import { isEqual, isNone, isNoneOrEmpty, useLocation } from '@karrio/lib';
import { TextAreaField } from '@karrio/ui/components/textarea-field';
import { WorkflowActionType } from '@karrio/hooks/workflow-actions';
import { AuthenticatedPage } from '@/layouts/authenticated-page';
import React, { useEffect, useReducer, useState } from 'react';
import { InputField } from '@karrio/ui/components/input-field';
import { useNotifier } from '@karrio/ui/components/notifier';
import { useLoader } from '@karrio/ui/components/loader';
import { AppLink } from '@karrio/ui/components/app-link';
import django from 'highlight.js/lib/languages/django';
import { SelectField } from '@karrio/ui/components';
import { NotificationType } from '@karrio/types';
import { Disclosure } from '@headlessui/react';
import hljs from "highlight.js";
import Head from 'next/head';

export { getServerSideProps } from "@/context/main";
hljs.registerLanguage('django', django);

type StateType = WorkflowType | UpdateWorkflowMutationInput;
type StateValueType = string | boolean | string[] | Partial<WorkflowType> | Partial<WorkflowActionType> | Partial<WorkflowTriggerType>;
const DEFAULT_STATE = {
  name: '',
  description: '',
  trigger: { trigger_type: "manual" },
  action_nodes: [{ order: 1, index: 0 }],
  actions: [{
    name: '',
    action_type: AutomationActionType.http_request,
    method: AutomationHTTPMethod.post,
    content_type: AutomationHTTPContentType.json,
    parameters_type: AutomationParametersType.data,
    parameters_template: `{
        "order_id": "{{ order_id }}",
    }`,
    header_template: `{
        "Content-Type": "application/json",
    }`,
  }],
} as Partial<StateType>;

function reducer(state: Partial<StateType>, { name, value }: { name: string, value: StateValueType }): Partial<StateType> {
  switch (name) {
    case 'partial':
      return { ...(value as StateType) };
    default:
      return { ...state, [name]: value }
  }
}

export default function Page(pageProps: any) {
  const Component: React.FC = () => {
    const loader = useLoader();
    const router = useLocation();
    const { id } = router.query;
    const notifier = useNotifier();
    const mutation = useWorkflowMutation();
    const [isNew, setIsNew] = useState<boolean>();
    const [workflow, dispatch] = useReducer(reducer, DEFAULT_STATE, () => DEFAULT_STATE);
    const { query: { data: { workflow: current } = {}, ...query }, workflowId, setWorkflowId } = useWorkflow({
      setVariablesToURL: true,
      id: id as string,
    });

    const zipActionWithNode = (actions: WorkflowActionType[], action_nodes: ActionNodeInput[]) => {
      const _tuple: [WorkflowActionType, ActionNodeInput][] = Array.from(Array(actions.length).keys()).map(index => {
        const action = actions[index];
        const node = (
          action_nodes.find((n) => ((!!n.slug && n.slug === action.slug) || (!!n.index && n.index === index)))
          || { order: index, slug: action.slug, index }
        );

        return [action, node]
      })

      return _tuple.sort((a, b) => a[1].order - b[1].order);
    };
    const handleChange = (event: React.ChangeEvent<any>) => {
      const target = event.target;
      let value = target.type === 'checkbox' ? target.checked : target.value;
      let name: string = target.name;

      if (target.multiple === true) {
        value = Array.from(target.selectedOptions).map((o: any) => o.value)
      }

      dispatch({ name, value });
    };
    const nestedChange = (name: string, index: number = -1) => (
      (event: React.ChangeEvent<any>) => handleChange(event)
    );
    const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
      evt.preventDefault();
      loader.setLoading(true);
      const { ...data } = workflow;

      try {
        if (isNew) {
          const { create_workflow } = await mutation.createWorkflow.mutateAsync(data as any);
          notifier.notify({ type: NotificationType.success, message: `Document workflow created successfully` });
          loader.setLoading(false);

          setWorkflowId(create_workflow.workflow?.id as string);
        } else {
          await mutation.updateWorkflow.mutateAsync(data as any);
          query.refetch();
          notifier.notify({ type: NotificationType.success, message: `Document workflow updated successfully` });
          loader.setLoading(false);
        }
      } catch (message: any) {
        notifier.notify({ type: NotificationType.error, message });
        loader.setLoading(false);
      }
    };
    const NextIndicator = () => (
      <div className="is-flex is-justify-content-space-around p-2 my-3">
        <span className="icon is-size-6">
          <i className="fas fa-lg fa-arrow-down"></i>
        </span>
      </div>
    );

    useEffect(() => { setIsNew(workflowId === 'new'); }, [workflowId]);
    useEffect(() => {
      if (query.isFetched && workflowId !== 'new') {
        dispatch({ name: 'partial', value: current as any });
      }
    }, [current, query.isFetched]);

    return (
      <form onSubmit={handleSubmit} className="p-4">

        <header className="columns has-background-white"
          style={{ position: 'sticky', zIndex: 1, top: 0, left: 0, right: 0, borderBottom: '1px solid #ddd' }}
        >
          <div className="column is-vcentered">
            <AppLink className="button is-small is-white" href="/workflows" style={{ borderRadius: '50%' }}>
              <span className="icon is-size-6">
                <i className="fas fa-lg fa-times"></i>
              </span>
            </AppLink>
            <span className="title is-4 has-text-weight-semibold px-3">Edit workflow</span>
          </div>
          <div className="column is-flex is-justify-content-end">
            <button
              type="submit"
              className="button is-small is-success"
              disabled={loader.loading || isEqual(workflow, workflow || DEFAULT_STATE)}
            >
              Save
            </button>
          </div>
        </header>

        <div className="columns m-0">

          {/* Workflow fields section */}
          <div className="column px-0 pb-4 is-relative">

            <InputField label="name"
              name="name"
              value={workflow.name as string}
              onChange={handleChange}
              placeholder="ERP orders sync"
              className="is-small"
              required
            />

            <TextAreaField label="description"
              name="description"
              value={workflow.description as string}
              onChange={handleChange}
              placeholder="Automate ERP orders syncing for fulfillment"
              className="is-small"
            />

          </div>

          <div className="p-3"></div>

          {/* Workflow related objects section */}
          <div className="column card is-9 px-3 py-4 has-background-light is-radiusless" style={{ height: '92vh', maxHeight: '92vh', overflowY: 'auto' }}>

            {/* Trigger section */}
            <Disclosure as='div' className="card px-0" defaultOpen={true} style={{ maxWidth: '500px', margin: 'auto' }}>
              <Disclosure.Button as='header' className="p-3 is-flex is-justify-content-space-between is-clickable">
                <div className="is-title is-size-6 is-vcentered my-2">
                  <span className="has-text-weight-bold">Trigger</span>
                  <p className="is-size-7 has-text-weight-semibold has-text-grey my-1">How the workflow is tiggered</p>
                </div>
              </Disclosure.Button>
              <Disclosure.Panel>
                <hr className='my-1' style={{ height: '1px' }} />

                <div className="p-3">

                  {/* trigger type */}
                  <SelectField name="trigger_type"
                    required={true}
                    label="Trigger type"
                    className="is-fullwidth"
                    fieldClass="column mb-0 px-0 py-2"
                    value={workflow.trigger?.trigger_type || ''}
                    onChange={nestedChange('trigger')}
                  >
                    {Array.from(new Set(Object.values(AutomationTriggerType))).map(
                      unit => <option key={unit} value={unit}>{unit}</option>
                    )}
                  </SelectField>

                  {/* trigger schedule */}
                  <div className="column mb-0 p-0" style={{
                    display: `${workflow.trigger?.trigger_type == AutomationTriggerType.scheduled ? 'block' : 'none'}`
                  }}>

                    <InputField name="schedule"
                      label="Schedule (cron)"
                      fieldClass="column mb-0 px-1 py-2"
                      defaultValue={workflow.trigger?.schedule || ''}
                      required={workflow.trigger?.trigger_type == AutomationTriggerType.scheduled}
                      onChange={nestedChange('trigger')}
                    />

                  </div>

                  {/* webhook options */}
                  <div className="column mb-0 p-0" style={{
                    display: `${workflow.trigger?.trigger_type == AutomationTriggerType.webhook ? 'block' : 'none'}`
                  }}>

                    <InputField name="secret"
                      label="Webhook secret"
                      fieldClass="column mb-0 px-1 py-2"
                      defaultValue={workflow.trigger?.secret || ''}
                      onChange={nestedChange('trigger')}
                    />

                    <InputField name="secret_key"
                      label="Webhook secret key"
                      fieldClass="column mb-0 px-1 py-0"
                      defaultValue={workflow.trigger?.secret_key || ''}
                      required={!isNoneOrEmpty(workflow.trigger?.secret_key)}
                      onChange={nestedChange('trigger')}
                    />

                  </div>

                </div>
              </Disclosure.Panel>
            </Disclosure>

            <NextIndicator />

            {/* Actions section */}
            {zipActionWithNode(workflow.actions as WorkflowActionType[], workflow.action_nodes as ActionNodeInput[]).map(([action, node], index) => (
              <React.Fragment key={index}>
                <Disclosure as='div' className="card px-0" style={{ maxWidth: '500px', margin: 'auto' }}>
                  <Disclosure.Button as='header' className="p-3 is-flex is-justify-content-space-between is-clickable">
                    <div className="is-title is-size-6 is-vcentered my-2">
                      <span className="has-text-weight-bold">Action</span>
                      <p className="is-size-7 has-text-weight-semibold has-text-grey my-1">
                        {action.name || 'An action to perform'}
                      </p>
                    </div>
                    <div>
                      <button type="button" className="button is-white" onClick={e => { e.stopPropagation(); }}>
                        <span className="icon"><i className="fas fa-pen"></i></span>
                      </button>
                      <button type="button" className="button is-white" onClick={e => { e.stopPropagation(); }}>
                        <span className="icon"><i className="fas fa-trash"></i></span>
                      </button>
                    </div>
                  </Disclosure.Button>
                  <Disclosure.Panel>
                    <hr className='my-1' style={{ height: '1px' }} />

                    <div className="p-3 is-size-7">

                      {/* action type */}
                      <div className="columns my-0 px-3">
                        <div className="column is-4 py-1">
                          <span className="has-text-weight-bold has-text-grey">Action type</span>
                        </div>
                        <div className="column is-8 py-1"><code>{action.action_type}</code></div>
                      </div>

                      {/* http request options */}
                      {action.action_type == AutomationActionType.data_mapping && <>

                        {/* action parameters type */}
                        <div className="columns my-0 px-3">
                          <div className="column is-4 py-1">
                            <span className="has-text-weight-bold has-text-grey">format</span>
                          </div>
                          <div className="column is-8 py-1"><code>{action.parameters_type}</code></div>
                        </div>

                        {/* action parameters template */}
                        <div className="columns is-multiline my-0 px-3">
                          <div className="column py-1">
                            <span className="has-text-weight-bold has-text-grey">Template</span>
                          </div>
                          <div className="column is-12 py-1">
                            <pre className="code p-1" style={{ maxHeight: '15vh', height: '15vh', overflowY: 'auto' }}>
                              <code
                                dangerouslySetInnerHTML={{
                                  __html: hljs.highlight(action.parameters_template as string, { language: 'django' }).value,
                                }}
                              />
                            </pre>
                          </div>
                        </div>

                      </>}

                      {/* http request options */}
                      {action.action_type == AutomationActionType.http_request && <>

                        {/* action method */}
                        <div className="columns my-0 px-3">
                          <div className="column is-4 py-1">
                            <span className="has-text-weight-bold has-text-grey">Method</span>
                          </div>
                          <div className="column is-8 py-1"><code>{action.method?.toLocaleUpperCase()}</code></div>
                        </div>

                        {/* action host */}
                        <div className="columns my-0 px-3">
                          <div className="column is-4 py-1">
                            <span className="has-text-weight-bold has-text-grey">Host</span>
                          </div>
                          <div className="column is-8 py-1"><code>{action.host}</code></div>
                        </div>

                        {/* host port */}
                        {!isNone(action.port) && <div className="columns my-0 px-3">
                          <div className="column is-4 py-1">
                            <span className="has-text-weight-bold has-text-grey">Port</span>
                          </div>
                          <div className="column is-8 py-1"><code>{action.port}</code></div>
                        </div>}

                        {/* action endpoint */}
                        {!isNoneOrEmpty(action.endpoint) && <div className="columns my-0 px-3">
                          <div className="column is-4 py-1">
                            <span className="has-text-weight-bold has-text-grey">Endpoint</span>
                          </div>
                          <div className="column is-8 py-1"><code>{action.endpoint}</code></div>
                        </div>}

                        {/* action content type */}
                        <div className="columns my-0 px-3">
                          <div className="column is-4 py-1">
                            <span className="has-text-weight-bold has-text-grey">Content Type</span>
                          </div>
                          <div className="column is-8 py-1"><code>{action.content_type}</code></div>
                        </div>

                        {/* action header template */}
                        <div className="columns is-multiline my-0 px-3">
                          <div className="column py-1">
                            <span className="has-text-weight-bold has-text-grey">Header Template</span>
                          </div>
                          <div className="column is-12 py-1">
                            <pre className="code p-1" style={{ maxHeight: '5vh', height: '5vh', overflowY: 'auto' }}>
                              <code
                                dangerouslySetInnerHTML={{
                                  __html: hljs.highlight(action.header_template as string, { language: 'django' }).value,
                                }}
                              />
                            </pre>
                          </div>
                        </div>

                        {/* action parameters type */}
                        <div className="columns my-0 px-3">
                          <div className="column is-4 py-1">
                            <span className="has-text-weight-bold has-text-grey">Parameters Type</span>
                          </div>
                          <div className="column is-8 py-1"><code>{action.parameters_type}</code></div>
                        </div>

                        {/* action parameters template */}
                        <div className="columns is-multiline my-0 px-3">
                          <div className="column py-1">
                            <span className="has-text-weight-bold has-text-grey">Parameters Template</span>
                          </div>
                          <div className="column is-12 py-1">
                            <pre className="code p-1" style={{ maxHeight: '15vh', height: '15vh', overflowY: 'auto' }}>
                              <code
                                dangerouslySetInnerHTML={{
                                  __html: hljs.highlight(action.parameters_template as string, { language: 'django' }).value,
                                }}
                              />
                            </pre>
                          </div>
                        </div>

                      </>}

                    </div>
                  </Disclosure.Panel>
                </Disclosure>

                <NextIndicator />
              </React.Fragment>
            ))}

            <div className="is-flex is-justify-content-space-around p-2">
              <button className="button is-small is-default">Add action</button>
            </div>

          </div>

        </div>

      </form>
    )
  };

  return AuthenticatedPage((
    <>
      <Head><title>{`Workflow - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>

      <Component />
    </>
  ), pageProps);
}