import './App.css';

const TableList = () => {

    const data = [
        {
            id: 1,
            url: "httpss",
            text: "aonweofinwe fadsf "
        },
        {
            id: 5,
            url: "asdfasdfasdfasdfasdf",
            text: "hello fadsf "
        },
        {
            id: 7,
            url: "ss",
            text: "hello fadsf "
        }
    ]

    const displayData = (data_list) => {
        return data_list.map((item) => {
            return (
                <tbody>
                    <tr>
                        <td>{item.id}</td>
                        <td>{item.url}</td>
                        <td>{item.text}</td>
                    </tr>
                </tbody>
            )
        })
    }

    return (
        <div>
            <table>
                <thead>
                <th>Company</th>
                <th>url</th>
                <th>Country</th>
                </thead>

                {displayData(data)}
            </table>
        </div>
    );
}

export default TableList;
