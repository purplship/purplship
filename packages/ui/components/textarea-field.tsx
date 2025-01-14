import React from "react";

interface TextAreaFieldComponent
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  fieldClass?: string;
  controlClass?: string;
}

export const TextAreaField = React.forwardRef(
  (
    {
      label,
      required,
      className,
      fieldClass,
      controlClass,
      children,
      ...props
    }: TextAreaFieldComponent,
    ref: React.ForwardedRef<HTMLTextAreaElement>,
  ): JSX.Element => {
    const Props = {
      required,
      ...props,
      ...(Object.keys(props).includes("value")
        ? { value: props.value || "" }
        : {}),
    };
    return (
      <div className={`field ${fieldClass}`}>
        {label !== undefined && (
          <label className="label is-capitalized is-size-7">
            {label}
            {required && (
              <span className="icon is-small has-text-danger small-icon">
                <i className="fas fa-asterisk" style={{ fontSize: ".7em" }}></i>
              </span>
            )}
          </label>
        )}
        <div className={`control ${controlClass}`}>
          <textarea className={`textarea ${className}`} {...Props} />
          {children}
        </div>
      </div>
    );
  },
);
