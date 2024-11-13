# coding: utf-8
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base(name='Model')


def get_id():
    return str(uuid.uuid4())


class XlsHeader(Model):
    __tablename__ = 'xls_header'
    Id = Column("id", String(256), index=True, primary_key=True)
    pul_master_id = Column(String(36))
    trip_id = Column(String(256))
    pickup_date = Column(String(256))
    router_id = Column(String(256))
    pickup_list = Column(String(256))
    deliver_date = Column(String(256))
    miles = Column(String(256))
    live_unload = Column(String(256))
    volume = Column(String(256))
    deliver_note = Column(String(256))
    qty = Column(String(256))
    mv_1 = Column(String(256))
    mv_2 = Column(String(256))
    mv_3 = Column(String(256))
    mv_4 = Column(String(256))
    shipper_1 = Column(String(256))
    shipper_2 = Column(String(256))
    shipper_3 = Column(String(256))
    shipper_4 = Column(String(256))
    mc_1 = Column(String(256))
    mc_2 = Column(String(256))
    mc_3 = Column(String(256))
    mc_4 = Column(String(256))
    dest_1 = Column(String(256))
    dest_2 = Column(String(256))
    dest_3 = Column(String(256))
    dest_4 = Column(String(256))

    def __init__(self):
        self.Id = get_id()


class XlsItem(Model):
    __tablename__ = 'xls_item'
    Id = Column("id", String(256), index=True, primary_key=True)
    header_id = Column(String(256))
    required_date = Column(String(256))
    part_no = Column(String(256))
    req_qty = Column(String(256))
    actual = Column(String(256))
    expected_type = Column(String(256))
    pack_qty = Column(String(256))
    container = Column(String(256))
    po = Column(String(256))
    line = Column(String(256))
    release = Column(String(256))

    def __init__(self):
        self.Id = get_id()


class PulLog(Model):
    __tablename__ = 'pul_log'
    Id = Column('id', String(256), index=True, primary_key=True)
    trans_time = Column(DateTime)
    log_in_status = Column(Integer)
    query_status = Column(Integer)
    total = Column(Integer)
    delivered = Column(Integer)
    revision_duplicated = Column(Integer)
    revision_changed = Column(Integer)
    fresh_item = Column(Integer)
    status = Column(Boolean)

    def __init__(self):
        self.Id = get_id()
        self.trans_time = datetime.now()
        self.status = 1
        self.total = 0
        self.delivered = 0
        self.revision_duplicated = 0
        self.revision_changed = 0
        self.fresh_item = 0
        self.save = 0


class PulMaster(Model):
    __tablename__ = 'pul_master'
    # 网站数据之外的两个字段
    Id = Column(String(256), index=True, primary_key=True)
    Available = Column(Boolean)
    LogId = Column('log_id', String(256))
    ImportTime = Column(DateTime)

    # 以下是网站数据
    LoadId = Column(String(256))
    ShipmentId = Column(String(256))
    OrderId = Column(String(256))
    LoadDisplayId = Column(String(256))
    Status = Column(String(256))
    OrderStatus = Column(String(256))
    Origin = Column(String(256))
    OriginCareOf = Column(String(256))
    Destination = Column(String(256))
    DestinationCareOf = Column(String(256))
    BillTo = Column(String(256))
    BeginDate = Column(String(256))
    EndDate = Column(String(256))
    Customer = Column(String(256))
    NextAction = Column(String(256))
    NextActionDate = Column(String(256))
    LoadRequestId = Column(String(256))
    ETAException = Column(String(256))
    HasPendingCustomerRequest = Column(String(256))
    PlanningType = Column(String(256))
    TotalCount = Column(String(256))
    Quantity = Column(String(256))
    Weight = Column(String(256))
    Hazmat = Column(String(256))
    UnNumber = Column(String(256))
    HazardClass = Column(String(256))
    PackingGroup = Column(String(256))
    ReferenceTypes = Column(String(256))
    Number = Column(String(256))
    FreightDimensions = Column(String(256))
    Length = Column(String(256))
    Width = Column(String(256))
    Height = Column(String(256))
    Diameter = Column(String(256))
    HandlingUnitCount = 0
    CurrentPhysicalLocationEntity = Column(String(256))
    CurrentPhysicalLoadTrackingNumber = Column(String(256))
    NextPhysicalLocationEntity = Column(String(256))
    LoadedOnTrailer = Column(String(256))
    LastKnownLocation = Column(String(256))
    ProcessOrderDetailId = Column(String(256))
    ProductNumber = Column(String(256))
    ShipmentTypeStatusText = Column(String(256))
    ConsolidationHub = Column(String(256))
    ProcessingHub = Column(String(256))
    ReleaseId = Column(String(256))
    PULCanBeConfirmedOrRejected = Column(String(256))
    IsPULConfirmed = Column(String(256))
    IsPULRejected = Column(String(256))
    PULConfirmedDate = Column(String(256))
    PULRejectedDate = Column(String(256))
    PULRevisionNumber = Column(String(256))
    IsBillToAperakConfigured = Column(String(256))
    HasRejectedOrConfirmed = Column(String(256))

    def __init__(self):
        self.Id = get_id()
        self.ImportTime = datetime.now()
        self.Available = 1


class PulDetail(Model):
    __tablename__ = 'pul_detail'
    Id = Column(String(256), index=True, primary_key=True)
    MasterId = Column(String(256))
    # 以下是网站数据
    ProcessOrderDetailID = Column(String(256))
    ProductId = Column(String(256))
    PONumber = Column(String(256))
    POLineNumber = Column(String(256))
    OrderSeqNumber = Column(String(256))
    ScheduleNumber = Column(String(256))
    ActualQuantity = Column(String(256))
    ExpectedQuantity = Column(String(256))
    ExpectedPrimaryPackagingId = Column(String(256))
    ExpectedSecondaryPackagingId = Column(String(256))
    ExpectedPickUpDate = Column(String(256))

    def __init__(self):
        self.Id = get_id()
