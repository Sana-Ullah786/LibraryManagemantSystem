import React, { ReactElement } from 'react'
import { ErrorObject } from '../CustomTypes'

interface Props {
    error?:ErrorObject
}


function ErrorComponent(props: Props): ReactElement {
    return (
        <div>
            <h2>
                {props?.error?.status}
            </h2>
            <h2>
                {props?.error?.message}
            </h2>
        </div>
    )
}

export default ErrorComponent
