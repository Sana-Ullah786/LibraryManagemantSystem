import React, { ReactElement } from "react";

export type Props = {
    page: number,
    setPage: React.Dispatch<React.SetStateAction<number>>
};

export function Pagination(props: Props): ReactElement {
    function previous() {
        if (props.page == 1) {
            return (
                <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', marginLeft: 20, marginRight: 20 }}>
                    <div>
                        <button id="prev" className='genre-link'> Prev </button>
                    </div>
                    <div>
                        <button onClick={() => { props.setPage(props.page + 1) }} className='genre-link'> Next </button>
                    </div>
                </div>
            )
        }

        else {
            return (
                <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', marginLeft: 20, marginRight: 20 }}>
                    <div>
                        <button id="prev" onClick={() => { props.setPage(props.page - 1) }} className='genre-link'> Prev </button>
                    </div>
                    <div>
                        <button onClick={() => { props.setPage(props.page + 1) }} className='genre-link'> Next </button>
                    </div>
                </div>
            )
        }
    }
    
    return(
        <div>
            {previous()}
        </div>
    )


    }

    