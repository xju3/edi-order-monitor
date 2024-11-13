#!/usr/bin/env python3
# coding: utf-8

import uuid

from common.base import Base
from domain.model.model import PulMaster, PulDetail, PulLog


class PulDao(Base):

    def __init__(self, callback, pul_log):
        super(PulDao).__init__()
        self.callback = callback
        self.pul_log = pul_log

    def save_pul_log(self, pul_log):
        self.env.session.add(pul_log)

    def get_pul_log(self, start_time, end_time):
        return self.env.session.query(PulLog).filter(PulLog.trans_time > start_time, PulLog.trans_time < end_time).all()

    def get_pul_master(self, shipment_id):
        return self.session.query(PulMaster). \
            filter(PulMaster.ShipmentId == shipment_id, PulMaster.Available == 1).first()

    def del_pul(self, shipment_id):
        master = self.get_pul_master(shipment_id)
        master.ImportStatus = -1
        self.session.update(master)
        self.session.commit()

    def save_pul(self, item):
        master = self._create_pul(item)
        self.callback("save pul: {0}".format(master.ShipmentId))
        self.session.add(master)

        detail_items = item['ProductView']
        if len(detail_items) == 0:
            self.session.rollback()
            return

        items_count = 0
        for detail_item in detail_items:
            detail = self._create_detail(master, detail_item)
            self.callback("save product item: {0}".format(detail.ProductId))
            self.session.add(detail)
            items_count += 1

        return master, items_count

    def _create_detail(self, master, item):
        # logger.debug(item)
        detail = PulDetail()
        detail.Id = str(uuid.uuid4())
        detail.MasterId = master.Id
        # 网站数据
        detail.ProcessOrderDetailID = item['ProcessOrderDetailID']
        detail.ProductId = item['ProductId']
        detail.PONumber = item['PONumber']
        detail.POLineNumber = item['POLineNumber']
        detail.OrderSeqNumber = item['OrderSeqNumber']
        detail.ScheduleNumber = item['ScheduleNumber']
        detail.ActualQuantity = item['ActualQuantity']
        detail.ExpectedQuantity = item['ExpectedQuantity']
        detail.ExpectedPrimaryPackagingId = item['ExpectedPrimaryPackagingId']
        detail.ExpectedSecondaryPackagingId = item['ExpectedSecondaryPackagingId']
        detail.ExpectedPickUpDate = item['ExpectedPickUpDate']
        return detail

    def _create_pul(self, item):
        # logger.debug(item)
        master = PulMaster()
        master.LogId = self.pul_log.Id
        # 网站数据
        master.LoadId = item['LoadId']
        master.ShipmentId = item['ShipmentId']
        master.OrderId = item['OrderId']
        master.LoadDisplayId = item['LoadDisplayId']
        master.Status = item['Status']
        master.OrderStatus = item['OrderStatus']
        master.Origin = item['Origin']
        master.OriginCareOf = item['OriginCareOf']
        master.Destination = item['Destination']
        master.DestinationCareOf = item['DestinationCareOf']
        master.BillTo = item['BillTo']
        master.BeginDate = item['BeginDate']
        master.EndDate = item['EndDate']
        master.Customer = item['Customer']
        master.NextAction = item['NextAction']
        master.NextActionDate = item['NextActionDate']
        master.LoadRequestId = item['LoadRequestId']
        master.ETAException = item['ETAException']
        master.HasPendingCustomerRequest = item['HasPendingCustomerRequest']
        master.PlanningType = item['PlanningType']
        master.TotalCount = item['TotalCount']
        master.Quantity = item['Quantity']
        master.Weight = item['Weight']
        master.Hazmat = item['Hazmat']
        master.UnNumber = item['UnNumber']
        master.HazardClass = item['HazardClass']
        master.PackingGroup = item['PackingGroup']
        master.ReferenceTypes = item['ReferenceTypes']
        master.Length = item['Length']
        master.Width = item['Width']
        master.Height = item['Height']
        master.Diameter = item['Diameter']
        master.HandlingUnitCount = item['HandlingUnitCount']
        master.CurrentPhysicalLocationEntity = item['CurrentPhysicalLocationEntity']
        master.CurrentPhysicalLoadTrackingNumber = item['CurrentPhysicalLoadTrackingNumber']
        master.NextPhysicalLocationEntity = item['NextPhysicalLocationEntity']
        master.LoadedOnTrailer = item['LoadedOnTrailer']
        master.LastKnownLocation = item['LastKnownLocation']
        master.ProcessOrderDetailId = item['ProcessOrderDetailId']
        master.ProductNumber = item['ProductNumber']
        master.ShipmentTypeStatusText = item['ShipmentTypeStatusText']
        master.ConsolidationHub = item['ConsolidationHub']
        master.ProcessingHub = item['ProcessingHub']
        master.ReleaseId = item['ReleaseId']
        master.PULCanBeConfirmedOrRejected = item['PULCanBeConfirmedOrRejected']
        master.IsPULConfirmed = item['IsPULConfirmed']
        master.IsPULRejected = item['IsPULRejected']
        master.PULConfirmedDate = item['PULConfirmedDate']
        master.PULRejectedDate = item['PULRejectedDate']
        master.PULRevisionNumber = item['PULRevisionNumber']
        master.IsBillToAperakConfigured = item['IsBillToAperakConfigured']
        master.HasRejectedOrConfirmed = item['HasRejectedOrConfirmed']
        return master
