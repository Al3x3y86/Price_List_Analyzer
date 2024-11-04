import os
import csv


class PriceMachine:

    def __init__(self):
        self.data = []

    def _search_product_price_weight(self, headers):
        product_keywords = ["название", "продукт", "товар", "наименование"]
        price_keywords = ["цена", "розница", "цена опт", "опт"]
        weight_keywords = ["вес", "фасовка", "масса"]

        product_idx = next((i for i, header in enumerate(headers) if header.lower() in product_keywords), None)
        price_idx = next((i for i, header in enumerate(headers) if header.lower() in price_keywords), None)
        weight_idx = next((i for i, header in enumerate(headers) if header.lower() in weight_keywords), None)

        return product_idx, price_idx, weight_idx

    def load_prices(self, file_path):
        for file_name in os.listdir(file_path):
            if 'price' in file_name.lower():
                with open(os.path.join(file_path, file_name), 'r', encoding='utf-8') as file:
                    reader = csv.reader(file, delimiter=',')
                    headers = next(reader)

                    print(f"Заголовок файла {file_name}: {headers}")

                    product_idx, price_idx, weight_idx = self._search_product_price_weight(headers)

                    if product_idx is None or price_idx is None or weight_idx is None:
                        print(f"Ошибка: файл {file_name} не содержит необходимые столбцы.")
                        continue

                    for row in reader:
                        try:
                            product = row[product_idx].strip()
                            price = float(row[price_idx])
                            weight = float(row[weight_idx])
                            price_per_kg = price / weight if weight != 0 else 0
                            self.data.append({
                                "product": product,
                                "price": price,
                                "weight": weight,
                                "file": file_name,
                                "price_per_kg": price_per_kg
                            })
                        except (IndexError, ValueError) as e:
                            print(f"Ошибка обработки строки в файле {file_name}: {e}")

    def find_text(self, text):
        results = [item for item in self.data if text.lower() in item["product"].lower()]
        sorted_results = sorted(results, key=lambda x: x["price_per_kg"])
        print(f"{'№':<4} {'Наименование':<30} {'Цена':<8} {'Вес':<5} {'Файл':<15} {'Цена за кг.'}")
        for i, item in enumerate(sorted_results, start=1):
            print(
                f"{i:<4} {item['product']:<30} {item['price']:<8} {item['weight']:<5} {item['file']:<15} {item['price_per_kg']:.2f}")

    def export_to_html(self, fname='output.html'):
        sorted_data = sorted(self.data, key=lambda x: x['price_per_kg'])
        html_content = '''
        <!DOCTYPE html>
        <html>
        <head><title>Прайс-лист</title></head>
        <body>
        <table border="1">
        <tr>
            <th>№</th>
            <th>Название</th>
            <th>Цена</th>
            <th>Вес</th>
            <th>Файл</th>
            <th>Цена за кг.</th>
        </tr>
        '''
        for i, item in enumerate(sorted_data, start=1):
            html_content += f'''
            <tr>
                <td>{i}</td>
                <td>{item["product"]}</td>
                <td>{item["price"]}</td>
                <td>{item["weight"]}</td>
                <td>{item["file"]}</td>
                <td>{item["price_per_kg"]:.2f}</td>
            </tr>
            '''
        html_content += '''
        </table>
        </body>
        </html>
        '''
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(html_content)


if __name__ == "__main__":
    pm = PriceMachine()
    pm.load_prices('C:\\Users\\Кузьминых\\PycharmProjects\\Diploma\\PriceListAnalyzer\\List')
    while True:
        query = input("Введите текст для поиска (или 'exit' для выхода): ")
        if query.lower() == "exit":
            print("Завершение работы.")
            break
        pm.find_text(query)
    pm.export_to_html('C:\\Users\\Кузьминых\\PycharmProjects\\Diploma\\PriceListAnalyzer\\List\\output.html')
