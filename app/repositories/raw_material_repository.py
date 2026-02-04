from app.repositories.base_repository import Repository
import pandas as pd
from typing import Literal
    
class RawMaterialRepository(Repository):
    name = 'rm_name'
    id = 'rm_id'
    
    def _rm_df_to_dict(self, df: pd.DataFrame) -> dict:
        '''
        Construye el diccionario que funciona para actualizar la base de datos
        '''
        return dict(zip(df['rm_name'], df['amount']))

    
    def _get_rm_amount(self, r_id: int, name: str) -> float:
        '''
        Obtiene la cantidad almacenada de una materia prima específica
        '''
        rm_amount = self.session.query(Stock.stock_amount)\
            .join(RawMaterial, RawMaterial.rm_id == Stock.rm_id)\
            .filter(
                RawMaterial.r_id == r_id,
                RawMaterial.rm_name == name
            ).scalar()
        return rm_amount

    def update_stock_amounts(
        self, 
        r_id: int,  
        df: pd.DataFrame,   
        direction: Literal["stock_in", "stock_out"] = "stock_in"
        ) -> None:
        '''
        Actualizando las cantidades de stock basadas en un DataFrame
        ''' 
        # Construyendo el diccionario
        rm_dict = self._rm_df_to_dict(df)

        # Consultando el stock perteneciente al restaurante y coincidiendoló al nombre de las respectivas materias primas
        stocks = (
            self.session.query(Stock)
            .join(RawMaterial, Stock.rm_id == RawMaterial.rm_id)
            .filter(
                RawMaterial.r_id == int(r_id),
                RawMaterial.rm_name.in_(rm_dict.keys())
            )
            .options(joinedload(Stock.raw_material))  
            .all()
        )

        # Actualizar las cantidades
        for stock in stocks:
            rm_name = stock.raw_material.rm_name
            amount = rm_dict.get(rm_name, 0)
            if direction == "stock_out":
                amount = -amount
            stock.stock_amount = float(stock.stock_amount) + amount