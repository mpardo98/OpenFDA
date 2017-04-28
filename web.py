#Copyright [2017] [Maria Pardo]
#Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
#except in compliance with the License. You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#Unless required by applicable law or agreed to in writing, software distributed under the License
#is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#KIND, either express or implied. See the License for the specific language governing
#permissions and limitations under the License.


#Conseguir que te devuelva los nombres de las compañías involucradas en el medicamento
import http.client
import http.server
import json
import socketserver

class OpenFDAClient():
        OPENFDA_API_URL= "api.fda.gov"
        OPENFDA_API_EVENT="/drug/event.json"


        def get_event(self,limite):
            #GET EVENT
            conn=http.client.HTTPSConnection(self.OPENFDA_API_URL)
            conn.request("GET",self.OPENFDA_API_EVENT+"?limit="+limite)
            r1 = conn.getresponse()
            data1=r1.read()
            data=data1.decode("utf8")
            return data

        def get_search_drug(self,url):

            lista_url= url.split("=")
            medicamento=lista_url[1]
            conn=http.client.HTTPSConnection(self.OPENFDA_API_URL)
            conn.request("GET",self.OPENFDA_API_EVENT+ "?search=patient.drug.medicinalproduct:"+medicamento+"&limit=10")
            r1 = conn.getresponse()
            data1=r1.read()
            data=data1.decode("utf8")
            search_drug=data
            return search_drug

        def get_search_company(self,url):
            list_url=url.split("=")
            negocio=list_url[1]
            conn=http.client.HTTPSConnection(self.OPENFDA_API_URL)
            conn.request("GET",self.OPENFDA_API_EVENT+"?search="+negocio+"&limit=10")
            r1 = conn.getresponse()
            data1=r1.read()
            data=data1.decode("utf8")
            negocios=data
            return negocios
# HTTPRequestHandler class


class OpenFDAParser():


    def get_medicinal_product(self,data):
        lista=[]
        events=json.loads(data)
        events= events["results"]
        for event in events:
            patient=event["patient"]
            drug=patient["drug"]
            medicinal_product=drug[0]["medicinalproduct"]
            lista+=[medicinal_product]
        return lista

    def get_companies(self,data):
        empresas = []
        events=json.loads(data)
        events= events["results"]
        for empresa in events:
            empresas.append(empresa["companynumb"])
        return empresas


    def get_list_search_drug(self,search_drug):
        companias=[]
        events=json.loads(search_drug)
        events= events["results"]
        for compania in events:
            companias.append(compania["companynumb"])
        return companias

    def get_list_search_company(self,negocios):
        lista=[]
        events=json.loads(negocios)
        events= events["results"]
        for event in events:
            patient=event["patient"]
            drug=patient["drug"]
            medicinal_product=drug[0]["medicinalproduct"]
            lista+=[medicinal_product]
        return lista

    def get_list_patient_sex(self,data):
        PatientSex=[]
        events=json.loads(data)
        events= events["results"]
        for patient in events:
            PatientSex.append(patient["patient"]["patientsex"])
        return PatientSex
        print ("*************************************************")
class OpenFDAHTML():

    def get_main_page(self):
        html="""
        <html>
            <head>
            </head>
            <body>
                <h1>OpenFDA Client</h1>
                <form method="get" action="listDrugs">
                    <body>Numero & eventos</body>
                    <input type="text" size=3 name="ProductList">
                    </input>
                    <input type="submit" value="Medicinal Product List">
                    </input>
                </form>
                <form method="get" action="listCompanies">
                    <body>Numero & eventos</body>
                    <input type="text" size="3" name="CompaniesList">
                    </input>
                    <input type="submit" value="Companies list">
                    </input>
                </form>
                <form method="get" action="searchDrug">
                    <input type="submit" value="Drug search: Send to OpenFDA">
                    </input>
                    <input type="text" name="drug">
                    </input>
                </form>
                <form method="get" action="searchCompany">
                    <input type="submit" value="Company search: Send to OpenFDA">
                    </input>
                    <input type="text" name="company">
                    </input>
                </form>
                <form method="get" action="listGender">
                    <body>Numero & eventos</body>
                    <input type="text" size=3 name="Limit">
                    </input>
                    <input type="submit" value="Patient sex">
                    </input>
                </form>
            </body>
        </html>
        """
        return html


    def get_html_medicinal_product(self,lista):
         s=''
         for med in lista:
             s+="<li>"+med+"</li>"

         html2="""
         <html>
              <head>
                    <tittle> Medicinal Product</tittle>
              </head>
              <body>
                    <h1>Medicinal Product</h1>
                    <ol>
                        %s
                    </ol>
              </body>
         </html>""" %(s)

         return html2
         #EL % SE INCLUYE PARA PODER METER UNA VARIABLE EN EL HTML

    def get_companies_name(self,empresas):
        html3="""
        <html>
            <head>
                <tittle>COMPANIES</tittle>
            </head>
            <body>
                <ol>
        """
        for empresa in empresas:
            html3+= "<li>" + empresa + "</li>\n"
        html3 += """
                </ol>
            </body>
        </html>
        """
        return html3
    def get_companias_name(self,companias):
        html4="""
        <html>
            <head>
                <tittle>COMPANIES</tittle>
            </head>
            <body>
                <ol>
        """
        for company in companias:
            html4+= "<li>" + company + "</li>\n"
        html4 += """
                </ol>
            </body>
        </html>
        """
        return html4
    def get_html_patient_sex(self,PatientSex):
        html5="""
        <html>
            <head>
                <tittle>PATIENT SEX</tittle>
            </head>
            <body>
                <ol>
        """
        for cliente in PatientSex:
            html5+= "<li>" + cliente + "</li>\n"
        html5 += """
                    </ol>
                </body>
            </html>
        """
        return html5
        #ol es para poner los numeros delante
    def html_error_404(self):
        html5="""
        <html>
            <head>
                <tittle>ERROR 404</tittle>
                <h1>ERROR 404</h1>
            </head>
            <body>El host ha sido capaz de comunicarse con el servidor, pero no existe el recurso que ha sido pedido</body>
        """
        return html5
        #wikipedia
class  testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):



    def get_limit(self):
        lista_url= self.path.split("=")
        limite=lista_url[1]
        print(limite)
        return limite

    def do_GET(self):
        HTML=OpenFDAHTML()
        CLIENT=OpenFDAClient()
        PARSER=OpenFDAParser()

        main_page=False
        is_event= False
        is_search_drug=False
        is_search_company=False
        is_company=False
        is_patient_sex=False
        secret=False
        redirect=False

        if self.path== '/':
            main_page=True
        elif '/listDrugs'in self.path:
            is_event=True
        elif '/listCompanies'in self.path:
            is_company=True
        elif '/searchDrug' in self.path:
            is_search_drug=True
        elif '/searchCompany' in self.path:
            is_search_company=True
        elif '/listGender' in self.path:
            is_patient_sex=True
        elif '/secret' in self.path:
            secret=True
        elif '/redirect' in self.path:
            redirect=True

        # Send response status code
        RESPOND=200

        if main_page:
            html=HTML.get_main_page()
        elif is_event:
            limite=self.get_limit()
            print(limite)
            print("*******************************************************")
            data=CLIENT.get_event(limite)
            list_drugs= PARSER.get_medicinal_product(data)
            html=HTML.get_html_medicinal_product(list_drugs)
            #medicinal_product=self.get_event()
        elif is_company:
             #mi path solo lo uso para CLIENT
            limite=self.get_limit()
            data=CLIENT.get_event(limite)
            companies=PARSER.get_companies(data)
            html= HTML.get_companies_name(companies)
        elif is_search_drug:
            url= self.path
            data=CLIENT.get_search_drug(url)
            companias=PARSER.get_list_search_drug(data)
            html=HTML.get_companias_name(companias)
        elif is_search_company:
            url= self.path
            data=CLIENT.get_search_company(url)
            negocios=PARSER.get_list_search_company(data)
            html=HTML.get_html_medicinal_product(negocios)
        elif is_patient_sex:
            limite=self.get_limit()
            data= CLIENT.get_event(limite)
            patientsex=PARSER.get_list_patient_sex(data)
            html= HTML.get_html_patient_sex(patientsex)
        elif secret:
            self.send_response(401)
            self.send_header('WWW-Authenticate','Basic realm="My realm"')
            self.end_headers()
        elif redirect:
            self.send_response(302)
            self.send_header('Location','/')
            self.end_headers()

        else:
            RESPOND=404
            html=HTML.html_error_404()

        self.send_response(RESPOND)
        self.send_header('Content-type','text/html')
        self.end_headers()
        if not secret and not redirect:
            self.wfile.write(bytes(html,"utf8"))


        return
