import pytest
from src.models import Empleado, Movimiento, Empresa, MovimientoValidado


class TestEmpleado:
    """Tests para el modelo Empleado."""
    
    def test_empleado_valido(self):
        """Test de empleado válido."""
        empleado = Empleado(
            nss="12345678901",
            nombre="Juan Pérez García",
            curp="PEGJ850301HDFRRN01"
        )
        
        assert empleado.nss == "12345678901"
        assert empleado.nombre == "Juan Pérez García"
        assert empleado.curp == "PEGJ850301HDFRRN01"
    
    def test_empleado_sin_curp(self):
        """Test de empleado sin CURP."""
        empleado = Empleado(
            nss="12345678901",
            nombre="Juan Pérez García"
        )
        
        assert empleado.nss == "12345678901"
        assert empleado.curp is None
    
    def test_nss_invalido(self):
        """Test de NSS inválido."""
        with pytest.raises(ValueError, match="El NSS debe tener exactamente 11 dígitos"):
            Empleado(
                nss="123456789",
                nombre="Juan Pérez García"
            )
    
    def test_nss_con_letras(self):
        """Test de NSS con letras."""
        with pytest.raises(ValueError, match="El NSS debe contener solo dígitos numéricos"):
            Empleado(
                nss="1234567890a",
                nombre="Juan Pérez García"
            )
    
    def test_curp_invalido(self):
        """Test de CURP inválido."""
        with pytest.raises(ValueError, match="El CURP debe tener exactamente 18 caracteres"):
            Empleado(
                nss="12345678901",
                nombre="Juan Pérez García",
                curp="PEGJ850301HDFRRN"
            )


class TestMovimiento:
    """Tests para el modelo Movimiento."""
    
    def test_movimiento_alta_valido(self):
        """Test de movimiento de alta válido."""
        empleado = Empleado(
            nss="12345678901",
            nombre="Juan Pérez García"
        )
        
        movimiento = Movimiento(
            tipo="alta",
            empleado=empleado,
            fecha_movimiento="2024-03-15",
            sbc=1500.0
        )
        
        assert movimiento.tipo == "alta"
        assert movimiento.sbc == 1500.0
        assert movimiento.motivo is None
    
    def test_movimiento_baja_valido(self):
        """Test de movimiento de baja válido."""
        empleado = Empleado(
            nss="12345678901",
            nombre="Juan Pérez García"
        )
        
        movimiento = Movimiento(
            tipo="baja",
            empleado=empleado,
            fecha_movimiento="2024-03-15",
            motivo="renuncia"
        )
        
        assert movimiento.tipo == "baja"
        assert movimiento.sbc is None
        assert movimiento.motivo == "renuncia"
    
    def test_tipo_movimiento_invalido(self):
        """Test de tipo de movimiento inválido."""
        empleado = Empleado(
            nss="12345678901",
            nombre="Juan Pérez García"
        )
        
        with pytest.raises(ValueError, match="El tipo de movimiento debe ser uno de"):
            Movimiento(
                tipo="invalido",
                empleado=empleado,
                fecha_movimiento="2024-03-15"
            )
    
    def test_fecha_invalida(self):
        """Test de fecha inválida."""
        empleado = Empleado(
            nss="12345678901",
            nombre="Juan Pérez García"
        )
        
        with pytest.raises(ValueError, match="La fecha debe tener formato YYYY-MM-DD"):
            Movimiento(
                tipo="alta",
                empleado=empleado,
                fecha_movimiento="15-03-2024",
                sbc=1500.0
            )
    
    def test_sbc_en_baja(self):
        """Test de SBC en baja (no permitido)."""
        empleado = Empleado(
            nss="12345678901",
            nombre="Juan Pérez García"
        )
        
        with pytest.raises(ValueError, match="Las bajas no deben incluir SBC"):
            Movimiento(
                tipo="baja",
                empleado=empleado,
                fecha_movimiento="2024-03-15",
                motivo="renuncia",
                sbc=1500.0
            )
    
    def test_sbc_maximo_excedido(self):
        """Test de SBC máximo excedido."""
        empleado = Empleado(
            nss="12345678901",
            nombre="Juan Pérez García"
        )
        
        with pytest.raises(ValueError, match="El SBC no puede exceder"):
            Movimiento(
                tipo="alta",
                empleado=empleado,
                fecha_movimiento="2024-03-15",
                sbc=3000.0
            )


class TestEmpresa:
    """Tests para el modelo Empresa."""
    
    def test_empresa_valida(self):
        """Test de empresa válida."""
        empleado = Empleado(
            nss="12345678901",
            nombre="Juan Pérez García"
        )
        
        movimiento = Movimiento(
            tipo="alta",
            empleado=empleado,
            fecha_movimiento="2024-03-15",
            sbc=1500.0
        )
        
        empresa = Empresa(
            registro_patronal="B5510768108",
            nombre="Tecnología Buk S.A. de C.V.",
            rfc="TBU050525AB1",
            movimientos=[movimiento]
        )
        
        assert empresa.registro_patronal == "B5510768108"
        assert empresa.nombre == "Tecnología Buk S.A. de C.V."
        assert empresa.rfc == "TBU050525AB1"
        assert len(empresa.movimientos) == 1
    
    def test_registro_patronal_invalido(self):
        """Test de registro patronal inválido."""
        empleado = Empleado(
            nss="12345678901",
            nombre="Juan Pérez García"
        )
        
        movimiento = Movimiento(
            tipo="alta",
            empleado=empleado,
            fecha_movimiento="2024-03-15",
            sbc=1500.0
        )
        
        with pytest.raises(ValueError, match="El registro patronal debe tener exactamente 11 caracteres"):
            Empresa(
                registro_patronal="B551076810",
                nombre="Tecnología Buk S.A. de C.V.",
                rfc="TBU050525AB1",
                movimientos=[movimiento]
            )
    
    def test_empresa_sin_movimientos(self):
        """Test de empresa sin movimientos."""
        with pytest.raises(ValueError, match="La empresa debe tener al menos un movimiento"):
            Empresa(
                registro_patronal="B5510768108",
                nombre="Tecnología Buk S.A. de C.V.",
                rfc="TBU050525AB1",
                movimientos=[]
            ) 